#!/usr/local/bin/python3

import math
import numpy
import matplotlib
import skimage.io


RESOLUTION_D = 100                     # number of detectors
RESOLUTION_A = 360                     # number of angular samples

INIT_ANGLE = math.pi / 2.0

DETECTORS = [
    position_of(i, INIT_ANGLE)
]


def load_object(filename):
    return skimage.io.imread(filename, as_grey=True)


def cast_ray(image, angle, detector):
    return 0.5
    




if __name__ == '__main__':
    print("Hello, world!")
