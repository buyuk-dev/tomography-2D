

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

