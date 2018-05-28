#!/usr/local/bin/python3

import argparse
import numpy

import matplotlib
import matplotlib.pyplot
import skimage.io

import mathutils
import ramp
import tomo


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to input image")
    args = parser.parse_args()
    return args 


def load_image_normalized(path):
    image = skimage.io.imread(path, as_grey=True)
    return numpy.interp(image, (image.min(), image.max()), (0, 255))


class Plotter:
    def __init__(self, grid):
        self.grid = grid
        self.cmap = 'gray'
        self.figure = matplotlib.pyplot.figure()

    def plot(self, data, n, title=None):  
        self.figure.add_subplot(*self.grid, n)
        if title is not None:
            matplotlib.pyplot.title(title)
        matplotlib.pyplot.imshow(data, cmap=self.cmap)

    def show(self):
        matplotlib.pyplot.show()


def main(path):
    original = load_image_normalized(path)
    space = numpy.pad(original, 50, 'constant')

    t = tomo.Tomograph()

    print("[config]")
    print("{} = {}".format("resolution", t.resolution))
    print("{} = {}".format("span", t.span))
    print("{} = {}".format("sampling", t.sampling))
    print("{} = {}".format("image", path))
    print("{} = {}".format("size", original.shape))
    print("------------")

    t.scan(space)
    print("scan done")
    filtered = ramp.filter(t.sinogram, t.resolution)
    print("ramp filter applied")
    rec = tomo.backprop(filtered, space.shape, t.sampling, t.span, t.resolution)
    print("reconstruction finished")
    rec = rec[50:-50,50:-50]
    rec = numpy.interp(rec, (rec.min(), rec.max()), (0, 255))

    rms = mathutils.rms_error(original, rec)
    print("RMS = {}".format(rms))

    return original, t.sinogram, filtered, rec



if __name__ == '__main__':
    cmd_args = parse_args()
    original, sinogram, filtered, rec = main(cmd_args.path)

    plotter = Plotter((2,2))
    plotter.plot(original, 1)
    plotter.plot(sinogram, 2)
    plotter.plot(filtered, 3)
    plotter.plot(rec, 4)
    plotter.show()
