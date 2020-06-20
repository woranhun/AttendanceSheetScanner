import tkinter as tk
from typing import Tuple

import cv2
import numpy as np

from assgui import ASSGUI

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]

if __name__ == "__main__":
    img = cv2.imread('testimg/7.png')
    root = tk.Tk()
    gui = ASSGUI(root, img)

    #    for point in GraphicsMath.findLineIntersections(Image.open('testimg/7.png')):
    #   cv2.circle(img, point, 1, (255, 0, 0), 1)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    root.mainloop()
