#!/usr/local/bin/python3

import math
import numpy
import matplotlib.pyplot
import skimage.io
import os


IMG_BASE_PATH = "img"
def get_path_to_object(object_name, extension="jpeg"):
    filename = object_name + "." + extension
    return os.path.join(IMG_BASE_PATH, filename)


RESOLUTION_D = 100 # number of detectors
RESOLUTION_A = 360 # number of angular samples


INIT_ANGLE = math.pi / 2.0 # initial angle 90 degrees


DETECTORS = [
]


def load_object(object_name):
    filename = get_path_to_object(object_name)
    return skimage.io.imread(filename, as_grey=True)


def cast_ray(image, angle, detector):
    return 0.5
    

if __name__ == '__main__':
    img = load_object("circle01")
    matplotlib.pyplot.imshow(img)
    matplotlib.pyplot.show()

