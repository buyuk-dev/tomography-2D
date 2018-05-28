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
        path = bresenham.bresenham_segment(source, detector)
        measurements.append(space[path[:,0], path[:,1]].sum())

    return measurements


class Tomograph:

    def __init__(self):
        self.resolution = 300
        self.sampling = 300
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


def backprop(sinogram, size, sampling, span, resolution):
    height, width = size
    img = [[0] * width for i in range(height)]

    step = (numpy.pi * 2.0) / sampling
    angles = [k * step for k in range(sampling)]

    for row, source_angle in zip(sinogram, angles):
        w, h = height - 5, width - 5
        center = Point(int(w/2), int(h/2))
        base = Point(int(w/2), 0)
        source = base.rotate(center, source_angle)
        halfspan = span / 2.0
        step = span / resolution
        detectors_apos = [
            source_angle + numpy.pi - halfspan + k * step
            for k in range(0, resolution)
        ]
        detectors = [base.rotate(center, angle) for angle in detectors_apos]
        for i, detector in enumerate(detectors):
            path = bresenham.bresenham_segment(source, detector)
            for p in path:
                img[p[0]][p[1]] += row[i]
    return numpy.array(img)

