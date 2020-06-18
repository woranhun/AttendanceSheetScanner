from typing import Tuple, List

import cv2
import numpy as np
import pytesseract
from PIL import Image

Point = Tuple[int, int]
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


def imageToStr(img: Image) -> str:
    ou = pytesseract.image_to_string(img)
    return ou


def imageToLines(pil_img: Image) -> List[Line]:
    img = np.array(pil_img)[:, :, ::-1].copy()
    out = list()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            out.append(((x1, y1), (x2, y2)))

    return out


if __name__ == "__main__":
    print(imageToStr(Image.open('testimg/1.png')))
    print(imageToLines(Image.open('testimg/2.png')))
