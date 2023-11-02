import serial
import time
from threading import Thread
from argparse import ArgumentParser
from frame import Frame

class SerialInterface:
    def __init__(self, port: str, cfg=None):
        self.port = port
        self.cfg = cfg


class CfgSerialInterface(SerialInterface):
    pass

class DataSerialInterface(SerialInterface):
    MAGIC_WORD = b'\x02\x01\x04\x03\x06\x05\x08\x07'
    HEADER_SIZE = 40
    TLV_TYPE_SIZE = 4
    TLV_LENGTH_SIZE = 4
    TLV_HEADER_SIZE = 8
    pass


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--port", default="/dev/ttyACM0", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-p", "--port", default="/dev/ttyACM1", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-c", "--cfg", default="AWR1642-SDK_2_1_0.cfg", type=str,
                            help="Specify config location")
