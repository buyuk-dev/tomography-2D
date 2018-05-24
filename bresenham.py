import mathutils
import numpy


def plotLineLow(A, B):
    dx, dy = (B.x - A.x), (B.y - A.y)
    
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    D = 2 * dy - dx
    y = A.y

    path = []
    for x in range(A.x, B.x + 1):
        path.append((x, y))
        if D > 0:
           y = y + yi
           D = D - 2*dx

        D = D + 2*dy

    return path


def plotLineHigh(A, B):
    dx, dy = (B.x - A.x), (B.y - A.y)

    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2*dx - dy
    x = A.x

    path = []
    for y in range(A.y, B.y + 1):
        path.append((x, y))
        if D > 0:
            x = x + xi
            D = D - 2*dy
        D = D + 2*dx
    return path


def bresenham_segment(A, B):
    if abs(B.y - A.y) < abs(B.x - A.x):
        if A.x > B.x:
            path = plotLineLow(B, A)
        else:
            path = plotLineLow(A, B)
    else:
        if A.y > B.y:
            path = plotLineHigh(B, A)
        else:
            path = plotLineHigh(A, B)
    return numpy.array(path)

