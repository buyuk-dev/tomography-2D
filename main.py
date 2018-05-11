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

import alg_sart # to implement

space = None

def cast_ray(source, detector, _placeholder):
    global space
    global is_marked
    path = bresenham.bresenham_segment(source, detector)
    #for p in path:
    #    space[p[0]][p[1]] = 200
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
    for source_angle in angles:
        measurements = scan(source_angle, space, ndetectors, span) 
        sinogram.append(measurements)
    return sinogram


class Tomograph:
    def __init__(self):
        self.resolution = 100
        self.span = math.pi
        self.sampling = 100

    def scan(self, space):
        self.space = space
        self.sinogram = compute_sinogram(
            self.space, 
            self.resolution,
            self.span,
            self.sampling
        ) 

    def construct(self):
        angles = [k * ((math.pi * 2.0) / self.sampling) 
                  for k in range(self.sampling)]
        return alg_sart.sart(numpy.array(self.sinogram), numpy.array(angles))
         

def display(img):
    matplotlib.pyplot.imshow(img)
    matplotlib.pyplot.show()


if __name__ == '__main__':

    t = Tomograph()
    
    space = loader.load_object("circle01", "jpeg")
    space = imgutils.scale_canvas(space, 100, 100)

    display(space)

    t.scan(space)
    display(t.sinogram)
 
    rec = t.construct()
    display(rec)


def foo():
    fig = matplotlib.pyplot.figure()
    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(space)

    fig.add_subplot(2, 2, 2)   
    matplotlib.pyplot.imshow(sinogram)

    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(reconstruction)
   

