import mathutils
import math
import numpy
import bresenham


def backprop(sinogram, size, sampling, span, resolution):
    height, width = size
    img = [[0] * width for i in range(height)]

    step = (numpy.pi * 2.0) / sampling
    angles = [k * step for k in range(sampling)]

    for row, source_angle in zip(sinogram, angles):
        w, h = height - 5, width - 5
        center = mathutils.Point(int(w/2), int(h/2))
        base = mathutils.Point(int(w/2), 0)
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
    return img

