import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Tuple, List

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


class ComputerVision(object):
    @staticmethod
    def imageToStr(input_img: Image) -> str:
        ou = pytesseract.image_to_string(input_img)
        return ou

    @staticmethod
    def imageToHoughLines(pil_img: Image) -> List[np.ndarray]:
        np_img = np.array(pil_img)[:, :, ::-1].copy()
        gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        return lines

    @staticmethod
    def imageToHoughLinesP(pil_img: Image, eps: float = 5) -> List[Line]:
        np_img = np.array(pil_img)[:, :, ::-1].copy()
        gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 720, 200, maxLineGap=eps)
        lines = [(np.array([line[0][0], line[0][1]]), np.array([line[0][2], line[0][3]])) for line in lines]
        return lines
