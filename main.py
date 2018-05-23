#!/usr/local/bin/python3

import numpy
import matplotlib.pyplot
import math
import numpy

import config
import imgutils
import mathutils
import loader
import dummy
import bresenham
import ramp
import backprop


def cast_ray(space, source, detector, _placeholder):
    path = bresenham.bresenham_segment(source, detector)
    absorption = 0.0
    for p in path:
        absorption += space[p[0]][p[1]]
    return absorption


def measure(source, detectors, space):
    measurements = []
    for detector in detectors:
        absorption = cast_ray(space, source, detector, space)
        measurements.append(absorption)    
    return measurements 


def scan(source_angle, space, ndetectors=10, span=math.pi/4.0):
    w = len(space) - 5
    h = len(space[0]) - 5
    center = mathutils.Point(int(w/2), int(h/2))    
    base = mathutils.Point(int(w/2), 0)
    source = base.rotate(center, source_angle) 

    halfspan = span / 2.0
    step = span / ndetectors
    detectors_apos = [
        source_angle + math.pi - halfspan + k * step 
        for k in range(0, ndetectors)
    ]
    detectors = [base.rotate(center, angle) for angle in detectors_apos]

    return measure(source, detectors, space)


def compute_sinogram(space, ndetectors, span,  nscans):
    step = (math.pi * 2.0) / nscans
    angles = [k * step for k in range(nscans)]

    sinogram = []
    for i, source_angle in enumerate(angles):
        print("source_angle: {} {}".format(source_angle, i))
        measurements = scan(source_angle, space, ndetectors, span) 
        sinogram.append(measurements)
    return sinogram


class Tomograph:
    def __init__(self):
        self.resolution = 200
        self.span = math.pi
        self.sampling = 200

    def scan(self, space):
        self.space = space
        self.sinogram = compute_sinogram(
            self.space, 
            self.resolution,
            self.span,
            self.sampling
        ) 
        return self.sinogram


if __name__ == '__main__':

    # load object
    original = loader.load_object("phantom", "png")
    ow, oh = len(original[0]), len(original)

    # run simulation
    space = imgutils.scale_canvas(original, 100, 100)
    sw, sh = len(space[0]), len(space)

    t = Tomograph()
    sinogram = t.scan(space)
    t.sinogram = ramp.filter(sinogram, t.resolution)
    filtered_sinogram = t.sinogram
    reconstruction = backprop.backprop(t.sinogram, (sh, sw), t.sampling, t.span, t.resolution)
    reconstruction = imgutils.cut(reconstruction, 50, 50, ow, oh)

    # display results
    fig = matplotlib.pyplot.figure()

    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(original, cmap="gray")

    fig.add_subplot(2, 2, 2)
    matplotlib.pyplot.imshow(sinogram, cmap="gray")

    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(filtered_sinogram, cmap="gray")
   
    fig.add_subplot(2, 2, 4)
    matplotlib.pyplot.imshow(reconstruction, cmap="gray")

    matplotlib.pyplot.show()

