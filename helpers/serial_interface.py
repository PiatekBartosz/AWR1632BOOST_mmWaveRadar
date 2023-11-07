import serial
import time
from threading import Thread
from .frame import Frame
from multiprocessing import Queue
import os
import struct


class SerialInterface:
    CFG_BOUDRATE = 115200
    DATA_BOUDRATE = 921600
    MAGIC_WORD = b'\x02\x01\x04\x03\x06\x05\x08\x07'
    HEADER_SIZE = 40
    TLV_TYPE_SIZE = 4
    TLV_LENGTH_SIZE = 4
    TLV_HEADER_SIZE = 8
    # TODO make a bool that indicates if the cfg was send
    # TODO make cfg for 3.6


    def __init__(self, cfg_port, data_port, cfg):
        self.cfg_serial = None
        self.data_serial = None
        self.sensor_started = False
        self.history = []

        try:
            self.cfg_serial = serial.Serial(cfg_port, self.CFG_BOUDRATE)
        except Exception as e:
            print("Exception, cfg port: ", e)

        try:
            self.data_serial = serial.Serial(data_port, self.DATA_BOUDRATE)
        except Exception as e:
            print("Exception, data port", e)

        self.cfg = cfg

        self.serial_enable = False

        self.cfg_rx = Queue()
        self.cfg_tx = Queue()

        self.data_rx = Queue()
        self.data_tx = Queue()

        # spawn processes to handle serial ports
        self.cfg_thread = Thread(target=self.cfg_uart_threadroutine)
        self.data_thread = Thread(target=self.data_uart_threadroutine)

    def cfg_uart_threadroutine(self):
        while self.serial_enable:
            self._read_from_cfg()
            self._write_to_cfg()
            time.sleep(0.05)

    def data_uart_threadroutine(self):
        while self.serial_enable:
            if self.sensor_started:
                self._read_from_data()
                self._write_to_data()
                time.sleep(0.05)

    def _read_from_cfg(self):
        byte_data = b""
        # check in while loop if umber of bytes in the input buffer is !- 0
        for i in range(2):
            while self.cfg_serial.in_waiting:

                byte = self.cfg_serial.read(1)
                byte_data += byte
                if byte == '\n'.encode():
                    break

        if byte_data != b"":
            data = byte_data.decode()
            self.cfg_rx.put(data)
            print("Cfg read data: ", data, end='')

    def _write_to_cfg(self):
        if not self.cfg_tx.empty():
            data = self.cfg_tx.get()
            self.history.append(data.decode())
            self.cfg_serial.write(data)
            if data == "sensorStart\n".encode():
                self.sensor_started = True
            print("Cfg send data: ", data.decode(), end='')


    def _read_from_data(self):
        found = False
        data = b""
        byte_count = 0

        while self.data_serial.in_waiting:
            data += self.data_serial.read(1)
            if not found and self.MAGIC_WORD in data:
                magic_word_idx = data.index(self.MAGIC_WORD)
                frame_header = magic_word = data[magic_word_idx:]
                found = True

                # parse header
                frame_header += self.data_serial.read(self.HEADER_SIZE - len(self.MAGIC_WORD))
                byte_count += self.HEADER_SIZE - len(self.MAGIC_WORD)

                version = struct.unpack('<I', frame_header[8:12])[0]
                total_packet_length = struct.unpack('<I', frame_header[12:16])[0]
                platform = struct.unpack('<I', frame_header[16:20])[0]
                frame_number = struct.unpack('<I', frame_header[20:24])[0]
                time_cpu_cycles = struct.unpack('<I', frame_header[24:28])[0]
                num_of_detected_objects = struct.unpack('<I', frame_header[28:32])[0]
                num_of_TLV = struct.unpack('<I', frame_header[32:36])[0]
                sub_frame_number = struct.unpack('<I', frame_header[36:40])[0]

                frame = Frame(magic_word, version, total_packet_length, platform, frame_number,
                              time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)

                # TODO more checks
                if total_packet_length > 10000:
                    raise Exception("Exceeded packet length")

                if total_packet_length % 32 != 0:
                    raise Exception("Packet size is not a multiple of 32")
                    found = False

                # read rest of the frame
                frame_tail = self.data_serial.read(total_packet_length - self.HEADER_SIZE)
                byte_count += total_packet_length - byte_count

                # get individual TVL's
                for i in range(num_of_TLV):
                    # type
                    tlv_type_packed = frame_tail[0:self.TLV_TYPE_SIZE]
                    tlv_type = struct.unpack('<I', tlv_type_packed)[0]

                    # get type of tlv
                    # TODO decipher type
                    tlv_length_packed = frame_tail[self.TLV_TYPE_SIZE:self.TLV_HEADER_SIZE]
                    tlv_length = struct.unpack('<I', tlv_length_packed)[0]

                    tlv_data = frame_tail[self.TLV_HEADER_SIZE:(self.TLV_HEADER_SIZE + tlv_length)]

                    # delete already read tlv from frame tail
                    frame.append_tvls(tlv_type, tlv_length, tlv_data, num_of_detected_objects)
                    frame_tail = frame_tail[(self.TLV_HEADER_SIZE + tlv_length):]

                self.data_rx.put(frame)
                found = False
                data = b''
                byte_count = 0

    def _write_to_data(self):
        if not self.data_tx.empty():
            data = self.data_tx.get()
            byte_data = data.encode()
            self.data_serial.write(byte_data)

    def start(self):
        # prepare cfg data to send
        try:
            abs_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../cfgs"))
            cfg_file_path = os.path.join(abs_parent_path, self.cfg)
            with open(cfg_file_path) as file:
                text = file.read()
                splited_text = text.split("\n")
                for line in splited_text:
                    if line[0] == '%':
                        continue

                    if line != '':
                        line_with_EOL = line + '\n'
                        self.cfg_tx.put(line_with_EOL.encode())

        except Exception as e:
            print(e)

        self.serial_enable = True
        self.cfg_thread.start()
        time.sleep(1)
        self.data_thread.start()

    def stop(self):
        self.serial_enable = False
        self.cfg_thread.join()
        self.data_thread.join()
        self.sensor_started = False
