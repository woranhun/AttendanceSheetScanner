from typing import Tuple

import cv2
from PIL import Image

from gmath import GraphicsMath

Point = Tuple[int, int]
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


if __name__ == "__main__":
    img = cv2.imread('testimg/2.png')
    for point in GraphicsMath.findLineIntersections(Image.open('testimg/2.png')):
        cv2.circle(img, point, 1, (255, 0, 0), 1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
