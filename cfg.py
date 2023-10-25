from argparse import ArgumentParser
import serial


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p --port", default="/dev/ttyACM0", type=str, 
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-c --cfg", default="AWR1642-SDK_3_2_0.cfg", type=str,
                            help="Specify config location")