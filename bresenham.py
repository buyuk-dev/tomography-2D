import mathutils


def plotLineLow(x0,y0, x1,y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = 2*dy - dx
    y = y0

    path = []
    for x in mathutils.closed_range(x0, x1, 1):
        path.append((x, y))
        if D > 0:
           y = y + yi
           D = D - 2*dx
        D = D + 2*dy
    return path

def plotLineHigh(x0,y0, x1,y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2*dx - dy
    x = x0

    path = []
    for y in mathutils.closed_range(y0, y1, 1):
        path.append((x, y))
        if D > 0:
            x = x + xi
            D = D - 2*dy
        D = D + 2*dx
    return path

def plotLine(x0,y0, x1,y1):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            return plotLineLow(x1, y1, x0, y0)
        else:
            return plotLineLow(x0, y0, x1, y1)
    else:
        if y0 > y1:
            return plotLineHigh(x1, y1, x0, y0)
        else:
            return plotLineHigh(x0, y0, x1, y1)


def bresenham_segment(A, B):
    return plotLine(A.x, A.y, B.x, B.y)

