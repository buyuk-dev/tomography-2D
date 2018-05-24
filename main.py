#!/usr/local/bin/python3

import numpy
import matplotlib.pyplot
import argparse

import skimage.io

import mathutils

import ramp
import backprop
import tomo


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to input image")
    args = parser.parse_args()
    return args 

def load_image_normalized(path):
    image = skimage.io.imread(cmd_args.path, as_grey=True)
    return numpy.interp(original, (original.min(), original.max()), (0, 255))

def main():
    cmd_args = parse_args()

    original = load_image_normalized(cmd_args.path)

    space = numpy.pad(original, 50, 'constant')
    t = tomo.Tomograph()
    t.scan(space)
    filtered = ramp.filter(t.sinogram, t.resolution)
    rec = backprop.backprop(filtered, space.shape, t.sampling, t.span, t.resolution)
    rec = rec[50:-50,50:-50]
    rec = numpy.interp(rec, (rec.min(), rec.max()), (0, 255))

    rms = mathutils.rms_error(original, rec)
    fig = matplotlib.pyplot.figure()
    fig.add_subplot(2, 2, 1)
    matplotlib.pyplot.imshow(original, cmap="gray")
    fig.add_subplot(2, 2, 2)
    matplotlib.pyplot.imshow(t.sinogram, cmap="gray")
    fig.add_subplot(2, 2, 3)
    matplotlib.pyplot.imshow(filtered, cmap="gray")
    fig.add_subplot(2, 2, 4)
    matplotlib.pyplot.imshow(rec, cmap="gray")
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()

