import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk

from gmath import GraphicsMath


class ASSGUI:

    def __init__(self, master, img):
        self.master = master
        self.label = tk.Label(self.master, text="Click me")
        self.label.pack()
        self.label.bind("<Button>", self.mouseClick)
        self.canvas = tk.Canvas(self.master, width=0, height=0)
        self.pilImage = np.array(img)[:, :, ::-1].copy()

        height, width, no_channels = img.shape
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.image = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack()
        self.canvas.bind("<Button>", self.mouseClick)

    def mouseClick(self, event):
        print("mouse clicked at x={0} y={1}".format(event.x, event.y))
        for point in GraphicsMath.findLineIntersections(self.pilImage):
            cv2.circle(self.pilImage, point, 1, (255, 0, 0), 1)
        self.image = Image.fromarray(self.pilImage)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
