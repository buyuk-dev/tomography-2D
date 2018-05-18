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
            print("backprop angle {}".format(source_angle))
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
         

def display(img):
    matplotlib.pyplot.imshow(img, cmap="gray")
    matplotlib.pyplot.show()


def compute_ramp(ndetectors):
    L = ndetectors * 2
    h = numpy.zeros(L)
    L2 = L // 2 + 1
    h[0] = 1/4.
    j = numpy.linspace(1, L2, L2//2, False)
    # h[2::2] = 0
    h[1:L2:2] = -1./(math.pi**2 * j**2)
    #h[-1:L2-1:-2] = -1./(pi**2 * j**2)
    h[L2:] = numpy.copy(h[1:L2-1][::-1])
    _ramp = h * 2.0
    return numpy.abs(numpy.fft.fft(_ramp))
    


def convolve2d(image, kernel):
    kernel = numpy.flipud(numpy.fliplr(kernel))
    output = numpy.zeros_like(image)
    
    image_padded = numpy.zeros((image.shape[0] + 2, image.shape[1] + 2))   
    image_padded[1:-1, 1:-1] = image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            output[y,x]=(kernel*image_padded[y:y+3,x:x+3]).sum()        
    return output


def normalize_row(row):
    pass


def normalize_sinogram(sinogram):
    norm = []
    for row in sinogram:
        norm.append(normalize_row(row, maximum))
    return norm


def filter_sinogram(sinogram, threshold=0):
    filtered = []
    for row in sinogram:
        fd = numpy.fft.fft(row)
        fd = [elem if elem > threshold else 0 for elem in row]
        sd = numpy.fft.ifft(fd).real
        print(sd)
        filtered.append(sd) 
    return filtered


def apply_filter(sinogram, ndetectors):
    ramp = compute_ramp(ndetectors)
    l_x = ndetectors
    filtered = numpy.fft.ifft(ramp * numpy.fft.fft(sinogram, 2*l_x, axis=1), axis=1)[:,:l_x].real
    return filtered


if __name__ == '__main__':

    t = Tomograph()
    
    space = loader.load_object("circle01", "jpeg")
    ow, oh = len(space[0]), len(space)
    space = imgutils.scale_canvas(space, 100, 100)

    t.scan(space)
    t.sinogram = apply_filter(t.sinogram, t.resolution)
    #t.sinogram = filter_sinogram(t.sinogram)
    #t.sinogram = imgutils.reject_extremes(t.sinogram, 25)
    display(t.sinogram)
   
    rec = t.backprop()
    rec = imgutils.cut(rec, 50, 50, ow, oh)
    #rec = imgutils.reject_extremes(rec, int((ow * oh) / 200.0))
    #rec = convolve2d(numpy.array(rec), numpy.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))
    display(rec)


def foo():
    fig = matplotlib.pyplot.figure()
    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(space)

    fig.add_subplot(2, 2, 2)   
    matplotlib.pyplot.imshow(sinogram)

    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(reconstruction)
   

