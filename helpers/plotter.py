import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import queue
import threading
from .frame import Frame

class RealTimeDataPlotter:
    def __init__(self, data_queue):
        self.fig, self.ax = plt.subplots()
        self.xs = []
        self.ys = []
        self.data_queue = data_queue

        # Set up plot to call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=20, fargs=(self.xs, self.ys), cache_frame_data=False)

    def animate(self, i, xs, ys):
        try:
            # Get random coordinates from the queue
            frame = self.data_queue.get_nowait()
            if not isinstance(frame, Frame):
                raise Exception("Real Time Data Plotter read wrong data type from data_rx_queue") 

            # TODO finish
            points = frame.tlvs[0].value.points

            for point in points:
                # Add x and y to lists
                xs.append(point["x"])
                ys.append(point["y"])

            # Limit x and y lists to 20 items
            xs = xs[-20:]
            ys = ys[-20:]

            # Draw scatter plot
            self.ax.clear()
            self.ax.scatter(xs, ys)

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Detection Points Scatter Plot')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.xlim([-5, 5])
            plt.ylim([0, 10])
        
        except queue.Empty:
            pass

    def show(self):
        plt.show()

# def data_generator(data_queue):
#     while True:
#         # Generate random coordinates
#         random_x = random.random()
#         random_y = random.random()

#         # Put the data in the queue
#         data_queue.put((random_x, random_y))

#         # Pause for 1 second to simulate the interval
#         threading.Event().wait(1)

# # used only for testing
# if __name__ == "__main__":
#     # Create a synchronized queue
#     synchronized_queue = queue.Queue()

#     # Start the data generator thread
#     data_generator_thread = threading.Thread(target=data_generator, args=(synchronized_queue,), daemon=True)
#     data_generator_thread.start()

#     # Create an instance of the RandomScatterPlot class with the synchronized queue
#     random_plotter = RealTimeDataPlotter(synchronized_queue)

#     # Show the plot
#     random_plotter.show()
