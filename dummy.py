
def draw(w, h, rx, ry, rw, rh, cx, cy, cw, ch):
    img = []

    # generate empty canvas
    for i in range(w):
        img.append([0.0] * h)
    
    # fill rect
    for x in range(rx, rx + rw):
        for y in range(ry, ry + rh):
            img[x][y] = 1.0

    # cut rect
    for x in range(cx, cx + cw):
        for y in range(cy, cy + ch):
            img[x][y] = 0.0

    return img


def create_dummy_1():
    return draw(300, 300, 100, 100, 100, 100, 130, 130, 30, 30)

