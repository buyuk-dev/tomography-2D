#!/usr/local/bin/python3

import numpy
import matplotlib.pyplot
import sys

import imgutils
import mathutils
import loader
import dummy

import ramp
import backprop
import tomo


if __name__ == '__main__':

    filename, extension = "phantom", "png"
    if len(sys.argv) == 2:
        print("loading {}".format(sys.argv[1]))
        filename, extension = sys.argv[1].split(".")

    # load object
    original = loader.load_object(filename, extension)
    ow, oh = len(original[0]), len(original)

    # run simulation
    space = imgutils.scale_canvas(original, 100, 100)
    sw, sh = len(space[0]), len(space)

    t = tomo.Tomograph()
    sinogram = t.scan(space)
    t.sinogram = ramp.filter(sinogram, t.resolution)
    filtered_sinogram = t.sinogram
    reconstruction = backprop.backprop(t.sinogram, (sh, sw), t.sampling, t.span, t.resolution)
    reconstruction = imgutils.cut(reconstruction, 50, 50, ow, oh)

    norm_original = mathutils.normalize(numpy.array(original), (0.0, 255.0))
    norm_reconstr = mathutils.normalize(numpy.array(reconstruction), (0.0, 255.0))
    rms = mathutils.rms_error(norm_original, norm_reconstr)
    print("RMS = {}".format(rms))

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

