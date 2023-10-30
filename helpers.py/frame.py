"""
    This class replicates the frame structure used in ti AWR1642demo in python

    TI UART Data Frame Structure

    ---------------
        -Header
    ---------------
        -Tag1
        -Len1           TVL
        -Payload1
    ---------------
        -Tag2
        -Len2           TVL
        -Payload2
    ---------------
        -Tag3      
        -Len3           TVL
        -Payload3
    ---------------
        Padding         x0F
    ---------------
        
    The Padding is added so that the total lenght of the frame is mulptile of 32 Bytes

   Header stucture:
    uint16_t    magicWord[4]; -> b'\x02\x01\x04\x03\x06\x05\x08\x07'
    uint32_t    version; -> 
    uint32_t    totalPacketLen;
    uint32_t    platform;
    uint32_t    frameNumber;
    uint32_t    timeCpuCycles;
    uint32_t    numDetectedObj;
    uint32_t    numTLVs;
    uint32_t    subFrameNumber;

    ! Little Endian !
"""
import struct
import os.path

class Header:
    pass

class TVL:
    pass
class Frame:

    def __init__(self, serial_frame_str) -> None:
        self.header = None
        self.tvl = None
        
        # parse serial data into header 
        self.header, self.tvl = self.parse_serial_data(serial_frame_str)
        pass

    def parse_serial_data(self, serial_frame_str) -> (Header, list[TVL]):
        # TODO check if data in correct format
        
        pass



class FrameType:
    pass

# this class opens a binary file with example test data from mmWave radar 
# and it is used to test the Frame class 
class TestFrameClass:
    def __init__(self):
        self.data = None
        self.TEST_DATA_FILE_NAME = "/../test_data/xwr16xx_processed_stream_2023_10_30T09_00_44_253.dat"
        with open(os.path.dirname(__file__) + self.TEST_DATA_FILE_NAME, "r", encoding = "ISO-8859-1") as file:
            self.data = file.read()

    @staticmethod
    def test_frame(serial_frame_str):
        Frame(serial_frame_str)



t1 = TestFrameClass()
print(t1.data)