#!/usr/local/bin/python3

import numpy
import matplotlib.pyplot
import sys
import argparse

import skimage.io

import mathutils
import dummy

import ramp
import backprop
import tomo


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to input image")
    args = parser.parse_args()
    return args 


if __name__ == '__main__':

    cmd_args = parse_args()
    original = skimage.io.imread(cmd_args.path, as_grey=True)

    space = numpy.pad(original, 50, 'constant')

    t = tomo.Tomograph()
    sinogram = t.scan(space)
    t.sinogram = ramp.filter(sinogram, t.resolution)
    filtered_sinogram = t.sinogram
    reconstruction = backprop.backprop(t.sinogram, space.shape, t.sampling, t.span, t.resolution)
    reconstruction = reconstruction[50:-50,50:-50]

    norm_original = mathutils.normalize(original, (0.0, 255.0))
    norm_reconstr = mathutils.normalize(reconstruction, (0.0, 255.0))
    rms = mathutils.rms_error(norm_original, norm_reconstr)

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

