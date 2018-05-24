import numpy
import bresenham
from mathutils import Point


def scan(angle, space, ndetectors, span):
    w, h = space.shape

    center = Point(w // 2, h // 2)    
    zero = Point(w // 2, 1)

    source = zero.rotate(center, angle) 
    step = span / ndetectors

    detectors = [
        angle + numpy.pi - (span / 2.0) + (k * step)
        for k in range(0, ndetectors)
    ]

    detectors = [
        zero.rotate(center, detector) 
        for detector in detectors
    ]

    measurements = []
    for detector in detectors:
        path = numpy.array(bresenham.bresenham_segment(source, detector))
        measurements.append(space[path[:,0], path[:,1]].sum())

    return measurements


class Tomograph:

    def __init__(self):
        self.resolution = 300
        self.sampling = 100
        self.span = numpy.pi

        step = (numpy.pi * 2.0) / self.sampling
        self.angles = [k * step for k in range(self.sampling)]

    def scan(self, space):
        self.space = space
        self.sinogram = [
            scan(angle, self.space, self.resolution, self.span)
            for angle in self.angles
        ] 
        return self.sinogram

