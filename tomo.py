import numpy
import math

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
        # SAMPLING --> RMS
        # 100 --> 59.43232439784853
        # 200 --> 49.46973185844213 
        # 300 --> 45.221974151266984
        # 400 --> 43.991697831156316
        self.resolution = 300
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
        return self.sinogram
