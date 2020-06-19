import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import List, Tuple

Point = Tuple[int, int]
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


class ComputerVision(object):
    @staticmethod
    def imageToStr(input_img: Image) -> str:
        ou = pytesseract.image_to_string(input_img)
        return ou

    @staticmethod
    def imageToHoughLines(pil_img: Image):
        np_img = np.array(pil_img)[:, :, ::-1].copy()
        gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        return lines

    @staticmethod
    def imageToLines(pil_img: Image) -> List[Line]:
        out = list()
        lines = ComputerVision.imageToHoughLines(pil_img)
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                out.append(((x1, y1), (x2, y2)))

        return out
