import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk
from typing import Callable, Tuple, List

from compvis import ComputerVision
from gmath import GraphicsMath
from numpyext import nparray_to_point
from pdfimg import PDFToIMG
from data import Student

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]


class ASSGUI(object):

    def __init__(self, master, img, size=None):
        self.master = master
        self.background_image = None if img is None else np.array(img)[:, :, ::-1].copy()
        self.photo = None

        if img is not None:
            height, width, no_channels = img.shape
        else:
            width = 300
            height = 300

        self.objects = list()
        if size is not None:
            self.master.geometry(size)

        self.canvas = tk.Canvas(self.master, width=width, height=height)

        self.label = None

        self.update_canvas()

    def createButton(self, text, col, row, callback):
        label = tk.Label(self.master, text=text)
        label.grid(row=row, column=col)
        label.bind("<Button-1>", callback)
        self.objects.append(label)
    def createDropDown(self, lst, col, row, var ):
        dropdown = tk.OptionMenu(self.master,var,*lst)
        dropdown.grid(row=row,column=col)
        self.objects.append(dropdown)


    def update_canvas(self):
        if self.background_image is not None:
            image = Image.fromarray(self.background_image)
            self.photo = ImageTk.PhotoImage(image)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.grid(row=1, column=0, columnspan=9)


class mainGUI(ASSGUI):

    def __init__(self, master, img):
        super(mainGUI, self).__init__(master, img)
        self.selector_gui = None
        self.base_image = img
        self.img = img
        self.grid = None
        self.students = []

        self.createButton("SetScanArea", 0, 0, self.ScanAreaClick)
        self.createButton("OpenPDF", 3, 0, self.OpenPDF)
        self.createButton("SelectImage", 4, 0, self.SelectImage)
        self.createButton("DetectSignatures", 6, 0, self.DetectSignatures)
        PDFToIMG.createDirs()

    def ScanAreaClick(self, _):
        root = tk.Toplevel()
        self.selector_gui = setAreaGUI(root, self.img, self.set_scan_area)
        root.mainloop()

    def OpenPDF(self, _):
        PDFToIMG.convertPDFToIMG(filedialog.askopenfilename())

    def SelectImage(self, _):
        self.img = cv2.imread(filedialog.askopenfilename())
        self.update_canvas()
        super(mainGUI, self).__init__(self.master, self.img)


    def DetectSignatures(self, _):
        if self.grid is not None:
            root = tk.Toplevel()
            self.selector_gui = DetectSignatures(root, self.base_image, self.grid, self.students, 0)
            root.mainloop()

    def set_scan_area(self, scan_area: Quad) -> None:
        try:
            pil_img = GraphicsMath.transform_to_rectangle(Image.fromarray(self.img), scan_area)
            img = np.array(pil_img)[:, :, ::-1].copy()
            self.base_image = img.copy()
            width, height = pil_img.size
            cv2.rectangle(img, (0, 0), (int(width), int(height)), (0, 0, 0), 3)
            points = GraphicsMath.findLineIntersections(img)
            self.grid = GraphicsMath.create_grid_from_points(points, 5)
        except:
            return

        for column in self.grid:
            for quad in column:
                points = [nparray_to_point(p) for p in quad]
                cv2.rectangle(img, points[0], points[2], (255, 0, 0), 2)

        self.background_image = img
        self.update_canvas()


class setAreaGUI(ASSGUI):

    def __init__(self, master, img, callback: Callable[[Quad], None]):
        self.texts = ["bal felső", "bal alsó", "jobb alsó", "jobb felső"]
        self.corners = []
        super(setAreaGUI, self).__init__(master, img)
        self.callback = callback
        self.objects= None
        self.canvas.bind("<Button-1>", self.mouseClickOnCanvas)

    def mouseClickOnCanvas(self, event) -> None:
        self.corners.append(np.array([event.x, event.y]))
        cv2.line(self.background_image, (event.x - 5, event.y - 5), (event.x + 5, event.y + 5), (255, 0, 0), 2)
        cv2.line(self.background_image, (event.x - 5, event.y + 5), (event.x + 5, event.y - 5), (255, 0, 0), 2)
        self.update_canvas()

        if len(self.corners) >= 4:
            self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                                    font="sans-serif 20 bold",
                                    text="Feldolgozás...",
                                    fill="red")
            self.master.after(20, self.finish)

    def finish(self):
        self.export_scan_area()
        self.master.destroy()

    def export_scan_area(self) -> None:
        self.callback((self.corners[0], self.corners[1], self.corners[2], self.corners[3]))

    def update_canvas(self):
        super(setAreaGUI, self).update_canvas()
        if len(self.corners) < 4:
            self.canvas.create_text(5, 5,
                                    font="sans-serif 20 bold",
                                    text=f"Kattintson az átalakítandó terület {self.texts[len(self.corners)]} sarkára",
                                    anchor=tk.NW)


class DetectSignatures(ASSGUI):

    def __init__(self, master, img: np.ndarray, grid: List[List[Quad]], students: List[Student], class_num: int):
        self.grid = grid
        self.students = students
        self.class_num = class_num
        self.included_students = []
        self.backup_image = img.copy()
        super(DetectSignatures, self).__init__(master, img, "800x600")

        for column in self.grid:
            for quad in column:
                points = [nparray_to_point(p) for p in quad]
                cv2.rectangle(img, points[0], points[2], (255, 0, 0), 2)

        for i in range(len(grid[0])):
            name_quad = self.grid[0][i]
            sign_quad = self.grid[1][i]
            name = ComputerVision.getNameFromArea((nparray_to_point(name_quad[0]), nparray_to_point(name_quad[2])),
                                                  self.background_image)
            print('"', name, '"', sep="")
            sign = ComputerVision.getSignatureFromArea((nparray_to_point(sign_quad[0]), nparray_to_point(sign_quad[2])),
                                                       self.background_image)

            for stud in students:
                if stud.name is name:
                    student = stud
                    break
            else:
                student = Student(name)
                students.append(student)

            student.set_signed(class_num, sign)

            self.included_students.append(student)

        self.canvas.bind("<Button-1>", self.mouseClickOnCanvas)
        self.createButton("Save",0,0, self.save)
        self.selected = tk.StringVar(master)
        self.dates=["1","2","3","4"]
        self.selected.set(self.dates[0])
        self.createDropDown(self.dates,1,0,self.selected)
        self.update_canvas()

    def mouseClickOnCanvas(self, event) -> None:
        for i, quad in enumerate(self.grid[1]):
            if quad[0][0] <= event.x <= quad[2][0] and quad[0][1] <= event.y <= quad[2][1]:
                student = self.included_students[i]
                student.set_signed(self.class_num, not student.signs[self.class_num])
                break
        self.update_canvas()

    def update_canvas(self) -> None:
        self.background_image = self.backup_image.copy()

        if len(self.included_students) == 0:
            return

        draw_img = self.background_image.copy()
        for i, quad in enumerate(self.grid[1]):
            if self.included_students[i].signs[self.class_num]:
                col = (0, 255, 0)
            else:
                col = (255, 0, 0)

            cv2.rectangle(draw_img, nparray_to_point(quad[0]), nparray_to_point(quad[2]),
                          color=col,
                          thickness=-1)

        cv2.addWeighted(draw_img, 0.5, self.background_image, 0.5, 0, self.background_image)

        super(DetectSignatures, self).update_canvas()
    def save(self, event) -> None:
        print("Mentes")
        self.master.destroy()
        print(self.selected.get())