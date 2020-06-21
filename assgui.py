import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Callable, List

from compvis import ComputerVision
from gmath import GraphicsMath

Point = np.ndarray


class ASSGUI:

    def __init__(self, master, img):
        self.img = img
        self.master = master

        self.buttons=list()

        self.canvas = tk.Canvas(self.master, width=0, height=0)
        self.pilImage = np.array(img)[:, :, ::-1].copy()

        height, width, no_channels = img.shape
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.image = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.grid(row=1, column=0, columnspan=5)
        self.canvas.bind("<Button-1>", self.mouseClickOnCanvas)
        self.scan_area = None
        self.newwindow = None
        self.label = None

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        for point in GraphicsMath.findLineIntersections(self.pilImage):
            cv2.circle(self.pilImage, tuple(point), 1, (255, 0, 0), 1)
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def ScanAreaClick(self):
        root = tk.Toplevel()
        self.newwindow = setAreaGUI(root, self.img, self.set_scan_area)
        root.mainloop()
    def GetNameFromArea(self, event):
        root = tk.Toplevel()
        self.newwindow = getNameGUI(root, self.img)
        root.mainloop()

    def createButton(self, text, col, row, callback):

        label = tk.Label(self.master, text=text)
        label.grid(row=row, column=col)
        label.bind("<Button-1>", callback)
        self.buttons.append(label)

class mainGUI(ASSGUI):
    def __init__(self,master,img):
        super().__init__(master,img)
        self.createButton("SetScanArea", 0, 0, self.ScanAreaClick)
        self.createButton("GetNameFromArea", 1, 0, self.GetNameFromArea)

    def set_scan_area(self, scan_area: List[Point]) -> None:
        self.scan_area = scan_area


class setAreaGUI(ASSGUI):

    def __init__(self, master, img, callback: Callable[[List[Point]], None]):
        super().__init__(master, img)
        self.corners = []
        self.clickcnt = 0
        self.callback = callback
        self.buttons = None

    def mouseClickOnCanvas(self, event) -> None:
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        self.corners.append(np.array([event.x, event.y]))
        cv2.circle(self.pilImage, (event.x, event.y), 6, (255, 0, 0), 1)
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.clickcnt += 1
        if self.clickcnt >= 4:
            self.export_scan_area()
            self.master.destroy()


class getNameGUI(ASSGUI):
    def __init__(self, master, img):
        super().__init__(master, img)
        self.clickcnt = 0
        self.points = list()
        self.buttons=None

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        cv2.circle(self.pilImage, (event.x, event.y), 6, (255, 0, 0), 1)
        self.points.append((event.x,event.y))
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.clickcnt += 1
        if self.clickcnt >= 2:
            ComputerVision.getNameFromArea(np.array(self.points),self.img)
            self.points = list()
            self.master.destroy()

    def export_scan_area(self) -> None:
        self.callback(self.corners)
