

def negative(img):
    negative_img = []
    for row in img:
        negative_row = [
            1.0 - pixel
            for pixel in row ]
        negative_img.append(negative_row)
    return negative_img


def scale_canvas(img, padx, pady):
    newimg = []
    h, w = len(img), len(img[0])

    pad_top = int(pady / 2)
    pad_bottom = pad_top
    pad_left = int(padx / 2)
    pad_right = pad_left

    nw, nh = w + padx, h + pady

    for i in range(pad_top):
        newimg.append([0] * nw)

    for row in img:
        nrow = ([0] * pad_left) + row + ([0] * pad_right)
        newimg.append(nrow)
        
    for i in range(pad_bottom):
        newimg.append([0] * nw)
  
    return newimg 
