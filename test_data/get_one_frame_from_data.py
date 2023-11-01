from multiprocessing import Queue
import struct


class Header:
    def __init__(self, magic_word, version, total_packet_length, platform, frame_number,
                 time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number) -> None:
        self.magic_word = magic_word
        self.version = version
        self.total_packet_length = total_packet_length
        self.platform = platform
        self.frame_number = frame_number
        self.time_cpu_cycles = time_cpu_cycles
        self.num_of_detected_objects = num_of_detected_objects
        self.num_of_TLV = num_of_TLV
        self.sub_frame_number = sub_frame_number


class TLV:
    def __init__(self, type, length, data) -> None:
        self.type = type
        self.length = length
        self.data = data


class RawFrame:
    def __init__(self, header: Header, tail: bytes):
        self.header = header
        self.tail = tail


class Frame:
    def __init__(self, magic_word, version, total_packet_length, platform, frame_number,
                 time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number) -> None:
        self.header = Header(magic_word, version, total_packet_length, platform, frame_number,
                             time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)
        self.tlvs = []
        self.tail = None

    def append_tvls(self, type, length, data):
        self.tlvs.append(TLV(type, length, data))

    def add_tail(self, tail):
        self.tail = tail

class SimualtedSerialPort:
    FILENAME = "/home/bartek/AGV/AWR1642BOOST_mmWaveRadar/test_data/xwr16xx_processed_stream_2023_10_30T09_00_44_253.dat"
    MAGIC_WORD = b'\x02\x01\x04\x03\x06\x05\x08\x07'
    HEADER_SIZE = 40
    TLV_TYPE_SIZE = 4
    TLV_LENGTH_SIZE = 4
    MAX_PACKET_LEN = 5000

    def __init__(self):
        # create FIFO queue for data stream, it will store parsed data Frames
        self.rx_data_queue = Queue()

    def serial_port_routine(self):
        with open(self.FILENAME, "rb") as file:
            found = False
            data = b''
            byte_count = 0

            # TODO change while True to something with serial
            while True:
                byte_of_data = file.read(1)
                if byte_of_data == '':
                    print("Reached EOF")
                    break

                data += byte_of_data
                byte_count += 1

                if not found and self.MAGIC_WORD in data:
                    magic_word_idx = data.index(self.MAGIC_WORD)
                    parsed_data = data[magic_word_idx:]
                    found = True

                    # parse header
                    header = self.MAGIC_WORD + file.read(self.HEADER_SIZE - len(self.MAGIC_WORD))
                    byte_count += self.HEADER_SIZE - len(self.MAGIC_WORD)

                    magic_word = header[0:8]
                    version = struct.unpack('<I', header[8:12])[0]
                    total_packet_length = struct.unpack('<I', header[12:16])[0]
                    platform = struct.unpack('<I', header[16:20])[0]
                    frame_number = struct.unpack('<I', header[20:24])[0]
                    time_cpu_cycles = struct.unpack('<I', header[24:28])[0]
                    num_of_detected_objects = struct.unpack('<I', header[28:32])[0]
                    num_of_TLV = struct.unpack('<I', header[32:36])[0]
                    sub_frame_number = struct.unpack('<I', header[36:40])[0]

                    frame_header = Header(magic_word, version, total_packet_length, platform, frame_number,
                                time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)

                    # TODO more checks
                    if total_packet_length > self.MAX_PACKET_LEN:
                        raise Exception("Exceeded max packet length")

                    if total_packet_length % 32 != 0:
                        raise Exception("Packet size is not a multiple of 32")
                    found = False

                    # read rest of the frame
                    frame_tail = file.read(total_packet_length - byte_count)
                    byte_count += total_packet_length - byte_count

                    raw_frame = RawFrame(frame_header, frame_tail)
                    self.rx_data_queue.put(raw_frame)

                    data = b''
                    byte_count = 0


                    # # get individual TVL's
                    # for i in range(num_of_TLV):
                    #     # TODO change for frame_tail
                    #     tlv_type_packed = frame_tail[0:4]
                    #     tlv_type = struct.unpack('<I', tlv_type_packed)[0]
                    #
                    #     # TODO decipher type
                    #     tlv_length_packed = frame_tail[4:8]
                    #     tlv_length = tlv_type = struct.unpack('<I', tlv_length_packed)[0]
                    #
                    #     tlv_data = frame_tail[8:(tlv_length - 8)]
                    #
                    #     frame.append_tvls(tlv_type, tlv_length, tlv_data)
                    #
                    #     # truncate current tail
                    #     frame_tail = frame_tail[(tlv_length - 8):]
                    #
                    # test = b''
                    # while True:
                    #     test += file.read(1)
                    #     if self.MAGIC_WORD in test:
                    #         print("found")
                    #         break



if __name__ == "__main__":
    s = SimualtedSerialPort()
    s.serial_port_routine()
