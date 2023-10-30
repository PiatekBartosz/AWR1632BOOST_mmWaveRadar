from argparse import ArgumentParser
import serial

def handle_serial(port):
    CLI_CFG_PORT_BOUDRATE = 921600
    print("Using port no.:", port)

    ser = serial.Serial(port, CLI_CFG_PORT_BOUDRATE)

    while True:
        byte_count = ser.inWaiting()
        encoded_data = ser.read(byte_count)
        if encoded_data != b'':
            print(encoded_data)

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--port", default="/dev/ttyACM1", type=str, 
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")

    args = arg_parser.parse_args()

    handle_serial(args.port)