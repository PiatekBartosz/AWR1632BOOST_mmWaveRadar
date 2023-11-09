from helpers.serial_interface import SerialInterface
from argparse import ArgumentParser
import time
import signal
import numpy as np
from helpers.plotter import DetectionPointsPlotter

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

    while True:
        if serial.data_rx.empty():
            continue
        else:
            frame = serial.data_rx.get()
            print(frame.tlvs)

    # detection_plotter = DetectionPointsPlotter(12, 5)
    # detection_plotter.show()




    # # plot results
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

