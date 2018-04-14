#!/usr/local/bin/python3

import math
import numpy
import matplotlib.pyplot
import skimage.io
import os
import itertools
import math

from point import *


DETECTORS_NUMBER = 10

SAMPLING = 10

ANGULAR_SPAN = math.pi / 4


IMG_BASE_PATH = "img"
def get_path_to_object(object_name, extension="jpeg"):
    filename = object_name + "." + extension
    return os.path.join(IMG_BASE_PATH, filename)


def get_line_params(A, B):
    if B.x == A.x:
        # line is parallel to OY axis.
        return None

    a = (B.y - A.y) / (B.x - A.x)
    b = A.y - a * A.x

    return a, b


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
 

def cast_ray(source, detector, space):
    path = bresenham_segment(source, detector)
    absorption = 0.0
    for p in path:
        absorption += space[p[0]][p[1]]
    return absorption


def measure(source, detectors, space):
    measurements = []
    for detector in detectors:
        absorption = cast_ray(source, detector, space)
        measurements.append(absorption)
    return measurements 


def scan(source_angle, space, ndetectors=10, span=math.pi/4.0):
    w = len(space) - 5
    h = len(space[0]) - 5
    center = Point(int(w/2), int(h/2))    
    base = Point(int(w/2), 0)
    source = base.rotate(center, source_angle) 

    halfspan = span / 2.0
    step = span / ndetectors
    detectors_apos = [source_angle + math.pi - halfspan + k * step for k in range(0, ndetectors)]
    detectors = [source.rotate(center, angle) for angle in detectors_apos]

    return measure(source, detectors, space)


def compute_sinogram(space, ndetectors, span,  nscans):
    step = (math.pi * 2.0) / nscans
    angles = [k * step for k in range(nscans)]

    sinogram = []
    for source_angle in angles:
        measurements = scan(source_angle, space, ndetectors, span) 
        sinogram.append(measurements)
    return sinogram


if __name__ == '__main__':
    img = load_object("circle01")

    w = len(img)
    h = len(img[0])

    #source = Point(0, 140)
    #detector = Point(224, 140)
    #absorption = cast_ray(source, detector, img)
    #print(absorption)

    sinogram = compute_sinogram(img, 1000, math.pi/2, 1000)

    matplotlib.pyplot.imshow(sinogram)
    matplotlib.pyplot.show()

    #matplotlib.pyplot.imshow(img)
    #matplotlib.pyplot.show()

