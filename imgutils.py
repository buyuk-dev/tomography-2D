

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


def cut(img, posx, posy, w, h):
    newimg = []
    for row in img[posy:posy + h]:
        newimg.append(row[posx:posx + w])
    return newimg


def reject_extremes(img, margin):
    linear = []
    for row in img:
       linear.extend(row)
    length = len(linear)
    replace = []
    for elem in sorted(linear)[length-margin:]:
        replace.append(elem)
    replace = set(replace)
    replacement = linear[length - margin - 1]
    newimg = []
    for row in img:
        newimg.append([elem if elem not in replace else replacement for elem in row])
    return newimg 

