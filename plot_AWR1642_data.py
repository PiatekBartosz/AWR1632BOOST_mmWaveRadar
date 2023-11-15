from helpers.frame import TLV_types
from helpers.serial_interface import SerialInterface
from argparse import ArgumentParser
import time
import signal
import numpy as np
from helpers.plotter import RealTimeDataPlotter 
from sys import getsizeof

serial = None


def handler(signum, frame):
    global serial
    serial.stop()
    exit(1)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-c", "--cfg_port", default="/dev/ttyACM0", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-d", "--data_port", default="/dev/ttyACM1", type=str,
                            help="Specify serial port used to send cfg to ti mmWave Radar using CLI")
    arg_parser.add_argument("-C", "--cfg", default="AWR1642-SDK_3_6_0.cfg", type=str,
                            help="Specify config location")
    args = arg_parser.parse_args()
    serial = SerialInterface(args.cfg_port, args.data_port, args.cfg)
    serial.start()

    signal.signal(signal.SIGINT, handler)

    new_time = 0
    prev_time = 0

    # TODO change later the sleep
    time.sleep(10)

    data_plotter = RealTimeDataPlotter(serial.data_rx)
    data_plotter.show()

    # while True:
    #     # print(serial.data_rx.len())
    #     frames = serial.data_rx.dequeue_all()
    #     for frame in frames:
    #         # check if type of TVL is DetectionPoint
    #         if frame.tlvs[0].type == 1:
    #             points = frame.tlvs[0].value.points
    #             for point in points:
    #                 print(point["x"])
    #                 print(point["y"])
    #                 continue
    #         new_time = time.time()
    #         print("FPS:", str(int(1/(new_time - prev_time))))
    #         prev_time = new_time




    # plt.style.use('_mpl-gallery')
    # plt.ion()
    #
    # frame = serial.data_rx.get()
    #
    # # fig, ax = plt.subplots()
    # # data = frame.get_detections()
    # # x = np.ndarray((len(data), ))
    # # y = np.ndarray((len(data), ))
    # # for idx, point in enumerate(data):
    # #     x[idx] = point['x']
    # #     y[idx] = point['y']
    # # ax.scatter(x, y)
    # # ax.set(xlim=(0, x.max() * 2), ylim=(0, y.max() * 2))
    # # plt.show()
    #
    # while True:
    #
    #
    #
    #     # time.sleep(0.1)
    #     # # plot data in a interval
    #     # frame = serial.data_rx.get()
    #     # data = frame.get_detections()
    #     # x = np.ndarray((len(data),))
    #     # y = np.ndarray((len(data),))
    #     # for idx, point in enumerate(data):
    #     #     x[idx] = point['x']
    #     #     y[idx] = point['y']
    #     # ax.set(xlim=(0, x.max() * 2), ylim=(0, y.max() * 2))
    #     # fig.canvas.draw()
    #     # fig.canvas.flush_events()

