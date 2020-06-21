import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Callable, List, Tuple

from compvis import ComputerVision
from gmath import GraphicsMath
from numpyext import nparray_to_point

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]


class ASSGUI(object):

    def __init__(self, master, img):
        self.master = master
        self.photo = None

        height, width, no_channels = img.shape

        self.buttons = list()
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.label = None

        self.background_image = np.array(img)[:, :, ::-1].copy()

        self.update_canvas()

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        for point in GraphicsMath.findLineIntersections(self.background_image):
            cv2.circle(self.background_image, nparray_to_point(point), 1, (255, 0, 0), 1)
        self.update_canvas()

    def createButton(self, text, col, row, callback):
        label = tk.Label(self.master, text=text)
        label.grid(row=row, column=col)
        label.bind("<Button-1>", callback)
        self.buttons.append(label)

    def update_canvas(self):
        image = Image.fromarray(self.background_image)
        self.photo = ImageTk.PhotoImage(image)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.grid(row=1, column=0, columnspan=5)
        self.canvas.bind("<Button-1>", self.mouseClickOnCanvas)


class mainGUI(ASSGUI):

    def __init__(self, master, img):
        super(mainGUI, self).__init__(master, img)
        self.selector_gui = None
        self.img = img

        self.createButton("SetScanArea", 0, 0, self.ScanAreaClick)
        self.createButton("GetNameFromArea", 1, 0, self.GetNameFromArea)

    def ScanAreaClick(self, _):
        root = tk.Toplevel()
        self.selector_gui = setAreaGUI(root, self.img, self.set_scan_area)
        root.mainloop()

    def GetNameFromArea(self, _):
        root = tk.Toplevel()
        self.selector_gui = getNameGUI(root, self.img)
        root.mainloop()

    def set_scan_area(self, scan_area: Quad) -> None:
        self.background_image = np.array(GraphicsMath.transform_to_rectangle(self.img, scan_area))
        self.update_canvas()


class setAreaGUI(ASSGUI):

    def __init__(self, master, img, callback: Callable[[Quad], None]):
        super(setAreaGUI, self).__init__(master, img)
        self.corners = []
        self.callback = callback
        self.buttons = None

    def mouseClickOnCanvas(self, event) -> None:
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        self.corners.append(np.array([event.x, event.y]))
        cv2.circle(self.background_image, (event.x, event.y), 6, (255, 0, 0), 1)
        self.update_canvas()

        if len(self.corners) >= 4:
            self.export_scan_area()
            self.master.destroy()

    def export_scan_area(self) -> None:
        self.callback((self.corners[0], self.corners[1], self.corners[2], self.corners[3]))


class getNameGUI(ASSGUI):

    def __init__(self, master, img):
        super().__init__(master, img)
        self.points = list()
        self.buttons = None

    def mouseClickOnCanvas(self, event):
        self.points.append(np.array([event.x, event.y]))

        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        cv2.circle(self.background_image, (event.x, event.y), 6, (255, 0, 0), 1)
        self.update_canvas()

        if len(self.points) >= 2:
            print(ComputerVision.getNameFromArea(self.points, self.background_image))
            self.master.destroy()
