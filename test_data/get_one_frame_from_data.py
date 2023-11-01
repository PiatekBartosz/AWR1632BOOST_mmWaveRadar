from multiprocessing import Queue
import struct



TLV_types = {
    1: "DetectedPoints",
    2: "RangeProfile",
    3: "NoiseProfile",
    4: "AzimuthStaticHeatMap",
    5: "RangeDoppler",
    6: "Stats",
    7: "DetectedPointsSideInfo",
    8: "AzimuthElevationStaticHeatMap",
    9: "TemperatureStats"
}
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


class Frame:
    def __init__(self, magic_word, version, total_packet_length, platform, frame_number,
                 time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number) -> None:
        self.header = Header(magic_word, version, total_packet_length, platform, frame_number,
                             time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)
        self.tlvs = []

    def append_tvls(self, type, length, data):
        self.tlvs.append(TLV(type, length, data))


class SimualtedSerialPort:
    FILENAME = "AWR1642_test_data_SDK_3_6_0.dat"
    MAGIC_WORD = b'\x02\x01\x04\x03\x06\x05\x08\x07'
    HEADER_SIZE = 40
    TLV_TYPE_SIZE = 4
    TLV_LENGTH_SIZE = 4
    TLV_HEADER_SIZE = 8

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
                    header = magic_word = data[magic_word_idx:]
                    found = True

                    # parse header
                    header += file.read(self.HEADER_SIZE - len(self.MAGIC_WORD))
                    byte_count += self.HEADER_SIZE - len(self.MAGIC_WORD)

                    version = struct.unpack('<I', header[8:12])[0]
                    total_packet_length = struct.unpack('<I', header[12:16])[0]
                    platform = struct.unpack('<I', header[16:20])[0]
                    frame_number = struct.unpack('<I', header[20:24])[0]
                    time_cpu_cycles = struct.unpack('<I', header[24:28])[0]
                    num_of_detected_objects = struct.unpack('<I', header[28:32])[0]
                    num_of_TLV = struct.unpack('<I', header[32:36])[0]
                    sub_frame_number = struct.unpack('<I', header[36:40])[0]

                    frame = Frame(magic_word, version, total_packet_length, platform, frame_number,
                                time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)

                    # TODO more checks
                    if total_packet_length > 10000:
                        raise Exception("Exceeded packet length")

                    if total_packet_length % 32 != 0:
                        raise Exception("Packet size is not a multiple of 32")
                    found = False

                    # read rest of the frame
                    frame_tail = file.read(total_packet_length - self.HEADER_SIZE)
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
                        frame.append_tvls(tlv_type, tlv_length, tlv_data)
                        frame_tail = frame_tail[(self.TLV_HEADER_SIZE + tlv_length):]

                    self.rx_data_queue.put(frame)
                    found = False
                    data = b''
                    byte_count = 0



if __name__ == "__main__":
    s = SimualtedSerialPort()
    s.serial_port_routine()
