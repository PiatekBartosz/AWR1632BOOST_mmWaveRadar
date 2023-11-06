import serial
import time
from threading import Thread
from .frame import Frame
from multiprocessing import Queue
import os


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
            self._read_from_data()
            self._write_to_data()
            # time.sleep(0.05)

    def _read_from_cfg(self):
        byte_data = b""
        # check in while loop if umber of bytes in the input buffer is !- 0
        while self.cfg_serial.in_waiting:
            byte = self.cfg_serial.read(1)
            byte_data += byte
            if byte == '\n'.encode():
                break

        if byte_data:
            data = byte_data.decode()
            self.cfg_rx.put(data)
            print("Cfg read data: ", data)

    def _write_to_cfg(self):
        if not self.cfg_tx.empty():
            data = self.cfg_tx.get()
            self.cfg_serial.write(data)
            print("Cfg send data: ", data.decode())


    def _read_from_data(self):
        found = False
        data = b""
        byte_count = 0

        while self.data_serial.in_waiting:
            data += self.data_serial.read(1)
            if not found and self.MAGIC_WORD in data:
                magic_word_idx = data.index(self.MAGIC_WORD)

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
                        self.cfg_tx.put(line.encode())

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
