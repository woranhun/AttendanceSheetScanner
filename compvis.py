from typing import Tuple, List

import cv2
import numpy as np
import pytesseract
from PIL import Image
from customtypes import Point, Line


class ComputerVision:

    @staticmethod
    def image_to_str(img: Image) -> str:
        ou = pytesseract.image_to_string(img, lang="hun", config="--psm 7")
        return ou

    @staticmethod
    def image_to_hough_lines(pil_img: Image) -> List[Point]:
        img = np.array(pil_img)[:, :, ::-1].copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        return lines

    @staticmethod
    def image_to_lines(pil_img: Image) -> List[Line]:
        out = list()
        lines = ComputerVision.image_to_hough_lines(pil_img)
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
                out.append((np.array([x1, y1]), np.array([x2, y2])))

        return out

    @staticmethod
    def get_name_from_area(points: Tuple[Tuple[int, int], Tuple[int, int]], img: np.ndarray) -> str:
        return ComputerVision.image_to_str(img[points[0][1]:points[1][1], points[0][0]:points[1][0]])

    @staticmethod
    def get_signature_from_area(points: Tuple[Tuple[int, int], Tuple[int, int]], img: np.ndarray,
                                white_threshold: int = 230, sign_threshold: float = 1, padding: int = 5):
        roi = img[points[0][1]:points[1][1], points[0][0]:points[1][0]]
        whitepxcnt = 0
        allpxcnt = 0
        for y in range(padding, roi.shape[0] - padding):
            for x in range(padding, roi.shape[1] - padding):
                allpxcnt += 1
                if roi[y][x][0] >= white_threshold and \
                        roi[y][x][1] >= white_threshold and \
                        roi[y][x][2] >= white_threshold:
                    whitepxcnt += 1
        return whitepxcnt / allpxcnt < sign_threshold
