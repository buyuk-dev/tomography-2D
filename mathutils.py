import math
import numpy


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, center, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        x = self.x - center.x
        y = self.y - center.y

        nx = x * c - y * s
        ny = x * s + y * c

        x = nx + center.x
        y = ny + center.y

        return Point(round(x), round(y))


def rms_error(X, Y):
    assert X.shape == Y.shape
    diff = X - Y
    square = sum(sum(diff ** 2))
    n = X.shape[0] * X.shape[1]
    return numpy.sqrt(square/ n)



