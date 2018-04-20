import mathutils


def bresenham_segment(A, B):
    if A.x > B.x:
        tmp = A
        A = B
        B = tmp

    line = mathutils.get_line_params(A, B)

    path = []
    for x in mathutils.closed_range(A.x, B.x, 1):
        if line is None:
            direction = 1
            if A.y > B.y:
                direction = -1
            for y in mathutils.closed_range(A.y, B.y, direction):
                path.append((x, y))
        else:
            yr = line[0] * x + line[1]
            y = round(yr)
            path.append((x, y))

    return path

