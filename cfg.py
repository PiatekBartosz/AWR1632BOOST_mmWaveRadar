from argparse import ArgumentParser
import serial

def parse_cofig(cfg_file):
    file = open("cfgs/" + cfg_file, "r")
    text = file.read()
    file.close()
    cfg_commands = []

    splited_text = text.split("\n")
    for line in splited_text:
        if line != '':
            if line[0] != '%':
                cfg_commands.append(line)
    return cfg_commands

def handle_serial(args, cfg_commands):
    CLI_CFG_PORT_BOUDRATE = 115200
    print("Using port no.:", args.port)
    ser = serial.Serial(port=args.port, baudrate=CLI_CFG_PORT_BOUDRATE)

    # send config:
    for command in cfg_commands:
        print("Send: ", command)
        ser.write(command.encode())
        read_serial(ser)
    
    # let user write commands manually
    while True:
        ser.write(input("Command you want to send: ").encode())
        read_serial(ser)

def read_serial(serial):
    byte_count = serial.inWaiting()
    if byte_count > 0:
        rx = serial.read(byte_count).decode()
        print("Read: ", rx)
        return rx

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--port", default="/dev/ttyACM0", type=str, 
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-c", "--cfg", default="AWR1642-SDK_3_2_0.cfg", type=str,
                            help="Specify config location")
    args = arg_parser.parse_args()

    cfg_commands = parse_cofig(args.cfg)

    handle_serial(args, cfg_commands)