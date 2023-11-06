from multiprocessing import Queue
import struct
import math
import codecs
import binascii



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

