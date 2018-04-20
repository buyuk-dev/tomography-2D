

def negative(img):
    negative_img = []
    for row in img:
        negative_row = [
            1.0 - pixel
            for pixel in row ]
        negative_img.append(negative_row)
    return negative_img

