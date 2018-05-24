import numpy

import mathutils
import bresenham


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


def scan(source_angle, space, ndetectors=10, span=numpy.pi/4.0):
    w = len(space) - 5
    h = len(space[0]) - 5
    center = mathutils.Point(int(w/2), int(h/2))    
    base = mathutils.Point(int(w/2), 0)
    source = base.rotate(center, source_angle) 

    halfspan = span / 2.0
    step = span / ndetectors
    detectors_apos = [
        source_angle + numpy.pi - halfspan + k * step 
        for k in range(0, ndetectors)
    ]
    detectors = [base.rotate(center, angle) for angle in detectors_apos]

    return measure(source, detectors, space)


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

