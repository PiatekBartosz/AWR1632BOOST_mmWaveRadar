import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class DetectionPointsPlotter:
    def __init__(self, v0, v02):
        self.v0 = v0
        self.v02 = v02
        self.t = np.linspace(0, 3, 40)
        self.g = -9.81
        self.z = self.g * self.t ** 2 / 2 + self.v0 * self.t
        self.z2 = self.g * self.t ** 2 / 2 + self.v02 * self.t

        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter(self.t[0], self.z[0], c="b", s=5, label=f'v0 = {self.v0} m/s')
        self.line2 = self.ax.plot(self.t[0], self.z2[0], label=f'v0 = {self.v02} m/s')[0]

        self.ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='x [m]', ylabel='y [m]')
        self.ax.legend()

        self.ani = FuncAnimation(self.fig, self.update, frames=40, interval=30)

    def update(self, frame):
        x = self.t[:frame]
        y = self.z[:frame]
        data = np.stack([x, y]).T
        self.scat.set_offsets(data)
        self.line2.set_xdata(self.t[:frame])
        self.line2.set_ydata(self.z2[:frame])
        return (self.scat, self.line2)

    def show(self):
        plt.show()

if __name__ == "__main__":
    # Usage:
    v0 = 12
    v02 = 5
    animated_plot = DetectionPointsPlotter(v0, v02)
    animated_plot.show()


