import matplotlib.pyplot


class Plotter:
    def __init__(self, grid):
        self.grid = grid
        self.cmap = 'gray'
        self.figure = matplotlib.pyplot.figure()

    def plot(self, data, n, title=None):  
        self.figure.add_subplot(*self.grid, n)
        if title is not None:
            matplotlib.pyplot.title(title)
            matplotlib.pyplot.axis("off")
        matplotlib.pyplot.imshow(data, cmap=self.cmap)

    def show(self):
        matplotlib.pyplot.show()

