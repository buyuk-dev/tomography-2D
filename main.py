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
        self.resolution = 500
        self.span = math.pi
        self.sampling = 500

    def scan(self, space):
        self.space = space
        self.sinogram = compute_sinogram(
            self.space, 
            self.resolution,
            self.span,
            self.sampling
        ) 

    def backprop(self):
        height, width = len(self.space), len(self.space[0])
        img = [[0] * width for row in self.space]

        step = (math.pi * 2.0) / self.sampling
        angles = [k * step for k in range(self.sampling)]

        for row, source_angle in zip(self.sinogram, angles):
            w = len(space) - 5
            h = len(space[0]) - 5
            center = mathutils.Point(int(w/2), int(h/2))    
            base = mathutils.Point(int(w/2), 0)
            source = base.rotate(center, source_angle) 
            halfspan = self.span / 2.0
            step = self.span / self.resolution
            detectors_apos = [
                source_angle + math.pi - halfspan + k * step 
                for k in range(0, self.resolution)
            ]
            detectors = [base.rotate(center, angle) for angle in detectors_apos]
            for i, detector in enumerate(detectors):
                path = bresenham.bresenham_segment(source, detector)
                for p in path:
                    img[p[0]][p[1]] += row[i]
        return img

    def construct(self):
        angles = [k * ((math.pi) / self.sampling) 
                  for k in range(self.sampling)]
        return alg_sart.sart(numpy.array(self.sinogram), numpy.array(angles))
         

if __name__ == '__main__':

    fig = matplotlib.pyplot.figure()
 
    space = loader.load_object("phantom", "png")
    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(space, cmap="gray")

    ow, oh = len(space[0]), len(space)
    space = imgutils.scale_canvas(space, 100, 100)

    t = Tomograph()
    t.scan(space)
    fig.add_subplot(2, 2, 2)
    matplotlib.pyplot.imshow(t.sinogram, cmap="gray")

    t.sinogram = ramp.filter(t.sinogram, t.resolution)
    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(t.sinogram, cmap="gray")
   
    rec = t.backprop()
    rec = imgutils.cut(rec, 50, 50, ow, oh)
    fig.add_subplot(2, 2, 4)
    matplotlib.pyplot.imshow(rec, cmap="gray")

    matplotlib.pyplot.show()

