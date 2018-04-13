#!/usr/local/bin/python3

import math
import numpy
import matplotlib.pyplot
import skimage.io
import os
import itertools
import math


IMG_BASE_PATH = "img"
def get_path_to_object(object_name, extension="jpeg"):
    filename = object_name + "." + extension
    return os.path.join(IMG_BASE_PATH, filename)


RESOLUTION_D = 100 # number of detectors
RESOLUTION_A = 360 # number of angular samples

RADIATION_SOURCE = (0, 1000)


DETECTORS = [
]


def get_line_params(A, B):
    if B.x == A.x:
        # line is parallel to OY axis.
        return None

    a = (B.y - A.y) / (B.x - A.x)
    b = A.y - a * A.x

    return a, b


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def closed_range(beg, end, step):
    if step > 0:
        return range(beg, end + 1, step)
    else:
        return range(beg, end - 1, step)


def bresenham_segment(A, B):
    if A.x > B.x:
        tmp = A
        A = B
        B = tmp

    line = get_line_params(A, B) 

    path = []
    for x in closed_range(A.x, B.x, 1):
        if line is None:
            direction = 1
            if A.y > B.y:
                direction = -1
            for y in closed_range(A.y, B.y, direction):
                path.append((x, y))
        else:
            yr = line[0] * x + line[1]
            y = round(yr)
            path.append((x, y))

    return path


def load_object(object_name):
    filename = get_path_to_object(object_name)
    return skimage.io.imread(filename, as_grey=True)
 

if __name__ == '__main__':
    img = load_object("circle01")

    w = len(img)
    h = len(img[0])

    path = bresenham_segment(Point(50, 100), Point(25, 25))
    for p in path:
        print(p)
        img[p[0]][p[1]] = 1.0

    matplotlib.pyplot.imshow(img)
    matplotlib.pyplot.show()

