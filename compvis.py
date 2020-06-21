from typing import Tuple, List

import cv2
import numpy as np
import pytesseract
from PIL import Image

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]


class ComputerVision:

    @staticmethod
    def imageToStr(img: Image) -> str:
        ou = pytesseract.image_to_string(img)
        return ou

    @staticmethod
    def imageToHoughLines(pil_img: Image) -> List[Point]:
        img = np.array(pil_img)[:, :, ::-1].copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
                out.append((np.array([x1, y1]), np.array([x2, y2])))

        return out
    @staticmethod
    def getNameFromArea(Points, img):
        print(Points)
        print(ComputerVision.imageToStr(img[Points[0][1]:Points[1][1],Points[0][0]:Points[1][0]]))
    @staticmethod
    def getSignitureFromArea(Points, img,treshold=230):
        ROI= img[Points[0][1]:Points[1][1],Points[0][0]:Points[1][0]]
        whitepxcnt=0
        allpxcnt=0
        for y in range(2,ROI.shape[0]):
            for x in range(2, ROI.shape[1]):
                allpxcnt+=1
                if ROI[y][x][0]>=treshold or ROI[y][x][1]>=treshold or ROI[y][x][2]>=treshold:
                    whitepxcnt+=1
        print(whitepxcnt,allpxcnt, whitepxcnt/allpxcnt)
        if whitepxcnt/allpxcnt < 1.0:
            return True
        else:
            return False

