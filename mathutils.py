import math


def get_line_params(A, B):
    if B.x == A.x:
        # line is parallel to OY axis.
        return None

    a = (B.y - A.y) / (B.x - A.x)
    b = A.y - a * A.x

    return a, b


def closed_range(beg, end, step):
    if step > 0:
        return range(beg, end + 1, step)
    else:
        return range(beg, end - 1, step)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, center, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        x = self.x - center.x
        y = self.y - center.y

        nx = x * c - y * s
        ny = x * s + y * c

        x = nx + center.x
        y = ny + center.y

        return Point(round(x), round(y))
