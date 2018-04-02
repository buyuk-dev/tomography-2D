#!/usr/local/bin/python3

import math
import numpy
import matplotlib.pyplot
import skimage.io


RESOLUTION_D = 100                     # number of detectors
RESOLUTION_A = 360                     # number of angular samples

INIT_ANGLE = math.pi / 2.0

DETECTORS = [
]


def load_object(filename):
    return skimage.io.imread(filename, as_grey=True)


def cast_ray(image, angle, detector):
    return 0.5
    

if __name__ == '__main__':
    img = load_object("img/circle01.jpeg")
    matplotlib.pyplot.imshow(img)
    matplotlib.pyplot.show()
