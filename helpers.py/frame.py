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
        self.type = TLV_types[type]
        self.length = length
        self.data = data


class Frame:
    def __init__(self, magic_word, version, total_packet_length, platform, frame_number,
                 time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number) -> None:
        self.header = Header(magic_word, version, total_packet_length, platform, frame_number,
                             time_cpu_cycles, num_of_detected_objects, num_of_TLV, sub_frame_number)
        self.tlvs = []

    def append_tlvs(self, type, length, data):
        self.tlvs.append(TLV(type, length, data))