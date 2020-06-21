import tkinter as tk
from typing import Tuple
import cv2
import numpy as np
from PIL import Image

from assgui import ASSGUI
from gmath import GraphicsMath
from numpyext import nparray_to_point

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]

if __name__ == "__main__":
  
    img = cv2.imread('testimg/7.png')
    root = tk.Tk()
    gui = ASSGUI(root, img)

    # img = cv2.imread('testimg/2.png')
    # points = GraphicsMath.findLineIntersections(Image.open('testimg/2.png'))
    # quads = GraphicsMath.create_grid_from_points(points)
    #
    # for quad in quads:
    #     coords = [nparray_to_point(p) for p in quad]
    #     cv2.line(img, coords[0], coords[1], (0, 0, 255), 1)
    #     cv2.line(img, coords[1], coords[2], (0, 0, 255), 1)
    #     cv2.line(img, coords[2], coords[3], (0, 0, 255), 1)
    #     cv2.line(img, coords[3], coords[0], (0, 0, 255), 1)
    #
    # for point in points:
    #     cv2.circle(img, nparray_to_point(point), 1, (255, 0, 0), 1)
    #
    # cv2.imshow('img', img)

    # for point in GraphicsMath.findLineIntersections(Image.open('testimg/7.png')):
    #     cv2.circle(img, point, 1, (255, 0, 0), 1)
    #     cv2.imshow('img', img)
    #     cv2.waitKey(0)
    root.mainloop()
