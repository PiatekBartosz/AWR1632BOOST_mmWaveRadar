import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import queue
import threading

class RandomScatterPlot:
    def __init__(self, data_queue):
        self.fig, self.ax = plt.subplots()
        self.xs = []
        self.ys = []
        self.data_queue = data_queue

        # Set up plot to call animate() function periodically
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, fargs=(self.xs, self.ys))

    def animate(self, i, xs, ys):
        try:
            # Get random coordinates from the queue
            random_x, random_y = self.data_queue.get_nowait()

            # Add x and y to lists
            xs.append(random_x)
            ys.append(random_y)

            # Limit x and y lists to 20 items
            xs = xs[-20:]
            ys = ys[-20:]

            # Draw scatter plot
            self.ax.clear()
            self.ax.scatter(xs, ys)

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Random Scatter Plot')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')

        except queue.Empty:
            pass

    def show(self):
        plt.show()

def data_generator(data_queue):
    while True:
        # Generate random coordinates
        random_x = random.random()
        random_y = random.random()

        # Put the data in the queue
        data_queue.put((random_x, random_y))

        # Pause for 1 second to simulate the interval
        threading.Event().wait(1)

if __name__ == "__main__":
    # Create a synchronized queue
    synchronized_queue = queue.Queue()

    # Start the data generator thread
    data_generator_thread = threading.Thread(target=data_generator, args=(synchronized_queue,), daemon=True)
    data_generator_thread.start()

    # Create an instance of the RandomScatterPlot class with the synchronized queue
    random_plotter = RandomScatterPlot(synchronized_queue)

    # Show the plot
    random_plotter.show()
