import binascii
import codecs
import math
import struct
import threading
from multiprocessing import Queue

import matplotlib.pyplot as plt
import numpy as np


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

class DetectedPoints:
    NAME = "DetectedPoints"
    SIZE = 16

    def __init__(self, raw_data, num_of_detected_objects):
        self.points = []
        # if len(raw_data) % self.SIZE:
        #     raise Exception("Detected point data wrong size")
        for i in range(num_of_detected_objects):
            raw_data_decoded = codecs.decode(binascii.hexlify(raw_data[0:self.SIZE]), encoding="hex")
            if raw_data_decoded == b'':
                break

            if len(raw_data_decoded) != 16:
                raise Exception("Invalid raw data")

            elements = struct.unpack("<ffff",raw_data_decoded)
            x = elements[0]
            y = elements[1]
            z = elements[2]
            v = elements[3]

            # calculate distance
            detected_range = math.sqrt((x * x) + (y * y) + (z * z))

            # calculate azimuth
            if y == 0.0:
                if x >= 0.0:
                    detected_azimuth = 90
                else:
                    detected_azimuth = -90
            else:
                detected_azimuth = math.atan(x / y) * 180 / math.pi

            point = {
                "x": x,
                "y": y,
                "z": z,
                "v": v,
                "detected_range": detected_range,
                "detected_azimuth": detected_azimuth
            }

            self.points.append(point)
            raw_data = raw_data[self.SIZE:]




    # @staticmethod
    # def parse_TLV(raw_data):
    #     data = {}
    #     try:
    #         # little endian h - short int (2 bytes), H - unsigned short int (2 bytes)
    #         elements = struct.unpack("<hHhh", raw_data)
    #     except struct.error as e:
    #         print("Exception while parsing TVL: ", e)
    #
    #     data = {
    #         "speedIdx": elements[0],
    #         "peakVal": elements[1],
    #         "x": elements[2],
    #         "y": elements[3]
    #     }
    #     return data

class RangeProfile:
    NAME = "RangeProfile"

    def __init__(self, raw_data):
        pass
    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for RangeProfile here
        pass

class NoiseProfile:
    NAME = "NoiseProfile"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for NoiseProfile here
        pass

class AzimuthStaticHeatMap:
    NAME = "AzimuthStaticHeatMap"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for AzimuthStaticHeatMap here
        pass

class RangeDoppler:
    NAME = "RangeDoppler"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for RangeDoppler here
        pass

class Stats:
    NAME = "Stats"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for Stats here
        pass

class DetectedPointsSideInfo:
    NAME = "DetectedPointsSideInfo"
    SIZE = 4

    def __init__(self, raw_data, num_of_detected_obj):
        self.points = []
        for i in range(num_of_detected_obj):
            # Signal to Noise Ratio
            # little endian, usinged int 16 bit
            snr, noise = struct.unpack("<HH", raw_data[0:self.SIZE])
            point = {
                "snr": snr,
                "noise": noise
            }
            self.points.append(point)
            raw_data = raw_data[self.SIZE:]

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for DetectedPointsSideInfo here
        pass

class AzimuthElevationStaticHeatMap:
    NAME = "AzimuthElevationStaticHeatMap"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for AzimuthElevationStaticHeatMap here
        pass

class TemperatureStats:
    NAME = "TemperatureStats"

    def __init__(self, raw_data):
        pass

    @staticmethod
    def parse_TLV(raw_data):
        # Add your implementation for parsing TLV for TemperatureStats here
        pass

TLV_types = {
    1: DetectedPoints,
    2: RangeProfile,
    3: NoiseProfile,
    4: AzimuthStaticHeatMap,
    5: RangeDoppler,
    6: Stats,
    7: DetectedPointsSideInfo,
    8: AzimuthElevationStaticHeatMap,
    9: TemperatureStats
}

class TLV:
    def __init__(self, type, length, raw_data, num_of_detected_obj) -> None:
        self.type = type
        self.length = length
        if type in TLV_types:
            if type == 1:
                self.value = TLV_types[type](raw_data, num_of_detected_obj)
            elif type == 7:
                self.value = TLV_types[type](raw_data, num_of_detected_obj)
            # for now skip other TLV types
            else:
                pass
        else:
            raise Exception("Frame type not found")


class Frame:
    def __init__(self, magic_word, version, total_packet_length, platform, frame_number,
                 time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number) -> None:
        self.header = Header(magic_word, version, total_packet_length, platform, frame_number,
                             time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)
        self.tlvs = []

    def append_tvls(self, type, length, raw_data, num_of_detected_obj):
        self.tlvs.append(TLV(type, length, raw_data, num_of_detected_obj))

    def get_detections(self):
        if self.tlvs:
            for tlv in self.tlvs:
                if tlv.type == 1:
                    return tlv.value.points
            return None
        return None


class SimualtedSerialPort:
    FILENAME = "/home/bartek/AGV/AWR1642BOOST_mmWaveRadar/test_data/AWR1642_test_data_SDK_3_6_0.dat"
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
                        frame.append_tvls(tlv_type, tlv_length, tlv_data, num_of_detected_objects)
                        frame_tail = frame_tail[(self.TLV_HEADER_SIZE + tlv_length):]
                        found = True

                    self.rx_data_queue.put(frame)
                    data = b''
                    byte_count = 0



if __name__ == "__main__":
    s = SimualtedSerialPort()
    th1 = threading.Thread(target=s.serial_port_routine)
    th1.start()

    frame = None

    while True:
        if not s.rx_data_queue.empty():
            frame = s.rx_data_queue.get()
            break

    # plot results
    plt.style.use('_mpl-gallery')

    fig, ax = plt.subplots()
    data = frame.get_detections()
    x = np.ndarray((len(data), ))
    y = np.ndarray((len(data), ))
    for idx, point in enumerate(data):
        x[idx] = point['x']
        y[idx] = point['y']
    ax.scatter(x, y)
    ax.set(xlim=(0, x.max() * 2), ylim=(0, y.max() * 2))
    plt.show()
