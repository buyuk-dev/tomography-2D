#!/usr/local/bin/python3

import math
import numpy
import matplotlib.pyplot
import skimage.io
import os
import itertools
import math
import numpy

import config
import imgutils
from point import *
import loader
import dummy

import alg_sart # to implement

space = None
has_been_marked = False


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

def cast_ray(source, detector):
    global has_been_marked
    global space
    path = bresenham_segment(source, detector)
    absorption = 0.0
    for p in path:
        absorption += space[p[0]][p[1]]
        # mark path
        if not has_been_marked:
            space[p[0]][p[1]] = 0.5
    return absorption


def measure(source, detectors, space):
    global has_been_marked
    measurements = []
    for detector in detectors:
        absorption = cast_ray(source, detector)
        measurements.append(absorption)
        
    has_been_marked = True
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
    # space = loader.load_object("export", "png")
    # space = imgutils.negative(space)
    space = dummy.create_dummy_1()
    w = len(space)
    h = len(space[0])

    nscans = 100
    sinogram = compute_sinogram(space, 100, math.pi, nscans)
     
    fig = matplotlib.pyplot.figure()
    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(space)

    fig.add_subplot(2, 2, 2)   
    matplotlib.pyplot.imshow(sinogram)

    angles = [k * ((math.pi * 2.0) / nscans) for k in range(nscans)]
    reconstruction = alg_sart.sart(numpy.array(sinogram), numpy.array(angles))

    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(reconstruction)
   
    matplotlib.pyplot.show()


