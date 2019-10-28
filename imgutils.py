import numpy


def pad(img, padding):
    return numpy.pad(img, padding, 'constant')


def crop(img, crop):
    return img[crop:-crop,crop:-crop]


def norm(img, range_=(0, 255)):
    return numpy.interp(img, (img.min(), img.max()), range_)

