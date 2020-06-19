import cv2
from PIL import Image

from gmath import GraphicsMath


if __name__ == "__main__":
    img = cv2.imread('testimg/3.png')
    quads = GraphicsMath.imageToQuads(Image.open('testimg/3.png'))
    for quad in quads:
        coords = [(int(p[0]), int(p[1])) for p in quad]
        cv2.line(img, coords[0], coords[1], (255, 0, 0), 1)
        cv2.line(img, coords[1], coords[2], (255, 0, 0), 1)
        cv2.line(img, coords[2], coords[3], (255, 0, 0), 1)
        cv2.line(img, coords[3], coords[0], (255, 0, 0), 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
