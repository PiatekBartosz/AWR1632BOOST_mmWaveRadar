from multiprocessing import Queue
import struct

filename = "/home/bartek/AGV/AWR1642BOOST_mmWaveRadar/test_data/xwr16xx_processed_stream_2023_10_30T09_00_44_253.dat"
MAGIC_WORD = b'\x02\x01\x04\x03\x06\x05\x08\x07'
HEADER_SIZE = 40

with open(filename, "rb") as file:
    data = file.read()
    magic_word_idx = data.index(MAGIC_WORD)

    # if magic word (frame start) is found
    if magic_word_idx == -1:
        raise Exception("Magic word not found")
    
    # cut data before magic word
    one_data_frame = data[magic_word_idx:]
    # "<" stand for little endian and I stands for Integer (32-bit)
    serial_header = struct.unpack('<I', one_data_frame)
    # TODO

    # search for packet lenght
    # get 
    pass





"""
import struct

# Define the expected header structure
header_format = '<4H I 3I'
header_size = struct.calcsize(header_format)
expected_magic_word = (0x0102, 0x0304, 0x0506, 0x0708)

# Specify the binary file path
file_path = 'your_binary_file.bin'

# Search for the header in the binary file
with open(file_path, 'rb') as file:
    while True:
        header_data = file.read(header_size)
        if not header_data:
            break  # Reached the end of the file

        header = struct.unpack(header_format, header_data)
        magic_word = header[:4]
        
        if magic_word == expected_magic_word:
            print("Header found at offset:", file.tell() - header_size)
            print("Magic Word:", magic_word)
            print("Version:", header[4])
            print("Total Packet Length:", header[5])
            print("Platform:", header[6])
            print("Frame Number:", header[7])
            print("Time CPU Cycles:", header[8])
            print("Number of Detected Objects:", header[9])
            print("Number of TLVs:", header[10])
            print("Sub-Frame Number:", header[11])
            break  # You can stop searching after the first header is found

"""
