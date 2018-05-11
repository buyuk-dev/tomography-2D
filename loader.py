import config
import skimage.io
import os


def get_path_to_object(object_name, extension=config.defaultImageFormat):
    filename = object_name + "." + extension
    return os.path.join(config.imagesBasePath, filename)

def load_object(object_name, extension=config.defaultImageFormat):
    filename = get_path_to_object(object_name, extension)
    image = skimage.io.imread(filename, as_grey=True)
    plist = []
    for row in image:
        plist.append(row.tolist())
    return plist

