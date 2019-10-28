#!/usr/local/bin/python3

import argparse
import numpy
import matplotlib.pyplot
import skimage.io

import mathutils
import imgutils
import ramp
import tomo
import plotter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to input image")
    args = parser.parse_args()
    return args 


def main(cfg, app):
    padding = 50

    original = skimage.io.imread(cfg.path, as_grey=True)
    space = imgutils.pad(original, padding)

    t = tomo.Tomograph(cfg.resolution, cfg.sampling, cfg.span)
    t.scan(space, app)
    filtered = ramp.filter(t.sinogram, t.resolution)

    if cfg.filter == "RAMP":
        rec = tomo.backprop(filtered, space.shape, t.sampling, t.span, t.resolution, app)
    else:
        rec = tomo.backprop(t.sinogram, space.shape, t.sampling, t.span, t.resolution, app)

    rec = imgutils.crop(rec, padding)
    rec = imgutils.norm(rec)

    rms = mathutils.rms_error(original, rec)

    return original, t.sinogram, filtered, rec, rms


if __name__ == '__main__':
    cmd_args = parse_args()
    original, sinogram, filtered, rec, rms = main(cmd_args)
    print("RMS = {}".format(rms))

