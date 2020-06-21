import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

from compvis import ComputerVision
from gmath import GraphicsMath
from pdfimg import PDFToIMG


class ASSGUI:

    def __init__(self, master, img,size=None):
        self.img = img
        self.master = master

        self.buttons = list()
        if size is not None:
            self.master.geometry(size)

        self.canvas = tk.Canvas(self.master, width=0, height=0)
        if img is not None:
            self.pilImage = np.array(img)[:, :, ::-1].copy()

            height, width, no_channels = img.shape
            self.canvas = tk.Canvas(self.master, width=width, height=height)
            self.image = Image.fromarray(img)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.grid(row=1, column=0, columnspan=5)
            self.canvas.bind("<Button-1>", self.mouseClickOnCanvas)

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        for point in GraphicsMath.findLineIntersections(self.pilImage):
            cv2.circle(self.pilImage, tuple(point), 1, (255, 0, 0), 1)
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def ScanAreaClick(self, event):
        root = tk.Toplevel()
        self.newwindow = setAreaGUI(root, self.img)
        root.mainloop()

    def GetNameFromArea(self, event):
        root = tk.Toplevel()
        self.newwindow = getNameGUI(root, self.img)
        root.mainloop()
    def ConvertPDF(self, event):
        root = tk.Toplevel()
        self.newwindow = convertPDF(root, None)
        root.mainloop()

    def createButton(self, text, col, row, callback):
        label = tk.Label(self.master, text=text)
        label.grid(row=row, column=col)
        label.bind("<Button-1>", callback)
        self.buttons.append(label)


class mainGUI(ASSGUI):
    def __init__(self, master, img):
        super().__init__(master, img)
        self.createButton("SetScanArea", 0, 0, self.ScanAreaClick)
        self.createButton("GetNameFromArea", 1, 0, self.GetNameFromArea)
        self.createButton("ConertPDF", 2, 0, self.ConvertPDF)
        PDFToIMG.createDirs()


class setAreaGUI(ASSGUI):
    def __init__(self, master, img):
        super().__init__(master, img)
        self.clickcnt = 0
        self.buttons = None

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        cv2.circle(self.pilImage, (event.x, event.y), 6, (255, 0, 0), 1)
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.clickcnt += 1
        if self.clickcnt >= 4:
            CALLBALINT()
            self.master.destroy()


class getNameGUI(ASSGUI):
    def __init__(self, master, img):
        super().__init__(master, img)
        self.clickcnt = 0
        self.points = list()
        self.buttons = None

    def mouseClickOnCanvas(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        cv2.circle(self.pilImage, (event.x, event.y), 6, (255, 0, 0), 1)
        self.points.append((event.x, event.y))
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.clickcnt += 1
        if self.clickcnt >= 2:
            ComputerVision.getNameFromArea(np.array(self.points), self.img)
            self.points = list()
            self.master.destroy()

class convertPDF(ASSGUI):
    def __init__(self, master, img):
        super().__init__(master,img,"300x300")
        self.createButton("OpenPDF", 0, 0, self.OpenPDF)
    def OpenPDF(self, event):
        PDFToIMG.convertPDFToIMG(filedialog.askopenfilename())
def CALLBALINT():
    print("Here comes Balint!")
