#!/usr/local/bin/python3

import argparse
import numpy

import matplotlib
import matplotlib.pyplot
import skimage.io

import mathutils
import ramp
import tomo
import plotter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to input image")
    args = parser.parse_args()
    return args 


def load_image_normalized(path):
    image = skimage.io.imread(path, as_grey=True)
    return numpy.interp(image, (image.min(), image.max()), (0, 255))


def main(cfg, app):
    original = load_image_normalized(cfg.path)
    space = numpy.pad(original, 50, 'constant')
    t = tomo.Tomograph(cfg.resolution, cfg.sampling, cfg.span)

    print("[config]")
    print("{} = {}".format("resolution", t.resolution))
    print("{} = {}".format("span", t.span))
    print("{} = {}".format("sampling", t.sampling))
    print("{} = {}".format("image", cfg.path))
    print("{} = {}".format("size", original.shape))
    print("------------")

    t.scan(space, app)
    print("scan done")
    
    filtered = ramp.filter(t.sinogram, t.resolution)
    print("ramp filter applied")

    if cfg.filter == "RAMP":
        print("RAMP filter enabled")
        rec = tomo.backprop(filtered, space.shape, t.sampling, t.span, t.resolution, app)
    else:
        rec = tomo.backprop(t.sinogram, space.shape, t.sampling, t.span, t.resolution, app)
    print("reconstruction finished")

    rec = rec[50:-50,50:-50]
    rec = numpy.interp(rec, (rec.min(), rec.max()), (0, 255))

    rms = mathutils.rms_error(original, rec)
    print("RMS = {}".format(rms))

    return original, t.sinogram, filtered, rec, rms



if __name__ == '__main__':
    cmd_args = parse_args()
    original, sinogram, filtered, rec, rms = main(cmd_args)

    plt = plotter.Plotter((2,2))
    plt.plot(original, 1)
    plt.plot(sinogram, 2)
    plt.plot(filtered, 3)
    plt.plot(rec, 4)
    plt.show()
