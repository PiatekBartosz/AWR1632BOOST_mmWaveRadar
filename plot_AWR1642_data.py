from helpers.serial_interface import SerialInterface
from argparse import ArgumentParser
import time


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-c", "--cfg_port", default="/dev/ttyACM0", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-d", "--data_port", default="/dev/ttyACM1", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-C", "--cfg", default="AWR1642-SDK_3_2_0.cfg", type=str,
                            help="Specify config location")
    args = arg_parser.parse_args()
    serial = SerialInterface(args.cfg_port, args.data_port, args.cfg)
    serial.start()
    time.sleep(10)
