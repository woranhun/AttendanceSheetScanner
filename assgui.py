import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, List

import cv2
import numpy as np
from PIL import Image, ImageTk

from compvis import ComputerVision
from customtypes import Quad
from data import Student
from filemgmt import FileMGMT
from gmath import GraphicsMath
from numpyext import nparray_to_point


class ASSGUI(object):

    def __init__(self, master, img, size=None):
        self.master = master
        self.background_image = None if img is None else np.array(img)[:, :, ::-1].copy()
        self.photo = None

        if img is not None:
            height, width, no_channels = img.shape
        else:
            width = 1000
            height = 1000

        if size is not None:
            self.master.geometry(size)

        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.grid(row=1, column=0, columnspan=6)

        self.update_canvas()

    def create_button(self, text, col, row, callback):
        button = tk.Button(self.master, text=text, command=callback)
        button.grid(row=row, column=col)

    def display_message(self, msg):
        self.canvas.create_rectangle(self.canvas.winfo_width() / 2 - 130, self.canvas.winfo_height() / 2 - 30,
                                     self.canvas.winfo_width() / 2 + 130, self.canvas.winfo_height() / 2 + 30,
                                     fill="white")
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                                font="sans-serif 20 bold",
                                text=msg,
                                fill="black")

    def create_dropdown(self, lst, col, row, var):
        dropdown = tk.OptionMenu(self.master, var, *lst)
        dropdown.grid(row=row, column=col)

    def update_canvas(self):
        if self.background_image is not None:
            image = Image.fromarray(self.background_image)
            self.photo = ImageTk.PhotoImage(image)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


class MainGUI(ASSGUI):

    def __init__(self, master, img, num_of_lectures):
        self.images = []
        self.current_index = 0
        self.selector_gui = None
        self.grid = None
        self.students = []
        self.current_scan_area = None
        self.transformed_area = None
        self.num_of_lectures = num_of_lectures

        self.page = tk.Label(master, text="Oldal: 0/0")
        self.page.grid(row=0, column=6)
        super(MainGUI, self).__init__(master, img)
        self.canvas.grid(row=1, column=1, columnspan=5)

        self.create_button("PDF hozzáadása", 0, 0, self.open_pdf)
        self.create_button("Kép hozzáadása", 1, 0, self.open_image)
        self.create_button("Táblázat bejelölése", 2, 0, self.set_area_click)
        self.create_button("Aláírások kigyűjtése", 3, 0, self.detect_signatures)
        self.create_button("Mentés", 4, 0, self.save)
        self.create_button("Törlés", 5, 0, self.clear)
        self.create_button("Előző", 0, 1, self.prev)
        self.create_button("Kövektező", 6, 1, self.next)
        FileMGMT.create_dirs()
        self.update_canvas()

    def add_image(self, img):
        data = {
            "img": img,
            "scan_areas": []
        }
        self.images.append(data)

    def get_current_image(self):
        if len(self.images) == 0:
            return None
        return self.images[self.current_index]["img"]

    def prev(self):
        self.current_index = max(self.current_index - 1, 0)
        self.update_canvas()

    def next(self):
        self.current_index = min(self.current_index + 1, len(self.images) - 1)
        self.update_canvas()

    def save(self) -> None:
        FileMGMT.save_to_csv(self.students, self.num_of_lectures)
        messagebox.showinfo("", "Mentve")

    def clear(self) -> None:
        self.students = []

    def open_pdf(self):
        images = FileMGMT.convert_pdf_to_img(filedialog.askopenfilename())
        for image in images:
            self.add_image(np.array(image))
        self.update_canvas()

    def open_image(self):
        img = Image.open(filedialog.askopenfilename())
        img.thumbnail((1000, 1000))
        self.add_image(np.array(img))
        self.update_canvas()

    def set_area_click(self):
        root = tk.Toplevel()
        self.selector_gui = SetAreaGUI(root, self.get_current_image(), self.receive_scan_area)
        root.mainloop()

    def receive_scan_area(self, scan_area: Quad) -> None:
        self.current_scan_area = scan_area
        self.update_canvas()
        self.display_message("Feldolgozás...")
        self.master.after(20, self.extract_grid)

    def extract_grid(self):
        pil_img = GraphicsMath.transform_to_rectangle(Image.fromarray(self.get_current_image()), self.current_scan_area)
        self.transformed_area = np.array(pil_img)[:, :, ::-1].copy()
        width, height = pil_img.size
        cv2.rectangle(self.transformed_area, (0, 0), (int(width), int(height)), (0, 0, 0), 3)
        points = GraphicsMath.find_line_intersection(self.transformed_area)
        self.grid = GraphicsMath.create_grid_from_points(points, 5)

        self.update_canvas()
        self.canvas.after(20, self.detect_signatures)

    def detect_signatures(self):
        if self.grid is not None and self.transformed_area is not None:
            root = tk.Toplevel()
            self.selector_gui = DetectSignaturesGUI(root, self.transformed_area, self.grid, self.students,
                                                    self.num_of_lectures, self.receive_signatures)
            root.mainloop()
            self.update_canvas()

    def receive_signatures(self, students: List[Student]):
        self.students = students
        self.images[self.current_index]["scan_areas"].append(self.current_scan_area)
        self.current_scan_area = None
        self.update_canvas()

    def update_canvas(self):
        self.background_image = self.get_current_image()
        self.page["text"] = f"Oldal: {self.current_index + 1}/{len(self.images)}"
        super(MainGUI, self).update_canvas()
        if self.current_scan_area is not None:
            p1 = nparray_to_point(self.current_scan_area[0])
            p2 = nparray_to_point(self.current_scan_area[1])
            p3 = nparray_to_point(self.current_scan_area[2])
            p4 = nparray_to_point(self.current_scan_area[3])
            self.canvas.create_polygon(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1],
                                       dash=(4, 4),
                                       outline="red",
                                       fill="",
                                       width=3)
        if len(self.images) > 0:
            for scan_area in self.images[self.current_index]["scan_areas"]:
                p1 = nparray_to_point(scan_area[0])
                p2 = nparray_to_point(scan_area[1])
                p3 = nparray_to_point(scan_area[2])
                p4 = nparray_to_point(scan_area[3])
                self.canvas.create_polygon(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1],
                                           dash=(4, 4),
                                           outline="green",
                                           fill="",
                                           width=5)


class SetAreaGUI(ASSGUI):

    def __init__(self, master, img, callback: Callable[[Quad], None]):
        self.texts = ["bal felső", "bal alsó", "jobb alsó", "jobb felső"]
        self.corners = []
        super(SetAreaGUI, self).__init__(master, img)
        self.callback = callback
        self.canvas.bind("<Button-1>", self.mouse_click_on_canvas)

    def mouse_click_on_canvas(self, event) -> None:
        self.corners.append(np.array([event.x, event.y]))
        cv2.line(self.background_image, (event.x - 5, event.y - 5), (event.x + 5, event.y + 5), (255, 0, 0), 2)
        cv2.line(self.background_image, (event.x - 5, event.y + 5), (event.x + 5, event.y - 5), (255, 0, 0), 2)
        self.update_canvas()

        if len(self.corners) >= 4:
            self.master.destroy()
            self.callback((self.corners[0], self.corners[1], self.corners[2], self.corners[3]))

    def update_canvas(self):
        super(SetAreaGUI, self).update_canvas()
        if len(self.corners) < 4:
            self.canvas.create_text(5, 5,
                                    font="sans-serif 20 bold",
                                    text=f"Kattintson a feldolgozandó terület {self.texts[len(self.corners)]} sarkára",
                                    anchor=tk.NW)


class DetectSignaturesGUI(ASSGUI):

    def __init__(self, master, img: np.ndarray, grid: List[List[Quad]], students: List[Student], num_of_lectures: int,
                 callback: Callable[[List[Student]], None]):
        self.grid = grid
        self.students = students
        self.signs = []
        self.backup_image = img.copy()
        self.callback = callback
        self.num_of_lectures = num_of_lectures
        super(DetectSignaturesGUI, self).__init__(master, img, "800x600")

        self.canvas.bind("<Button-1>", self.mouse_click_on_canvas)
        self.selected = tk.StringVar(master)
        self.dates = [str(class_index + 1) for class_index in range(num_of_lectures)]
        self.selected.set(self.dates[0])

        self.create_button("Mégse", 1, 0, self.cancel)
        self.create_dropdown(self.dates, 2, 0, self.selected)
        self.create_button("Elfogadás", 3, 0, self.finish)
        self.display_message("Feldolgozás...")
        self.master.after(20, self.extract_signatures)

    def extract_signatures(self):
        for i in range(len(self.grid[0])):
            name_quad = self.grid[0][i]
            sign_quad = self.grid[1][i]
            name = ComputerVision.get_name_from_area((nparray_to_point(name_quad[0]), nparray_to_point(name_quad[2])),
                                                     self.background_image)
            sign = ComputerVision.get_signature_from_area((nparray_to_point(sign_quad[0]),
                                                           nparray_to_point(sign_quad[2])), self.background_image)
            obj = {
                "name": name,
                "sign": sign
            }
            self.signs.append(obj)
        self.update_canvas()

    def finish(self):
        for sign in self.signs:
            name = sign["name"]
            sign = sign["sign"]
            for stud in self.students:
                if stud.name is name:
                    student = stud
                    break
            else:
                student = Student(name, self.num_of_lectures)
                self.students.append(student)
            student.set_signed(int(self.selected.get()) - 1, sign)
        self.master.destroy()
        self.callback(self.students)

    def mouse_click_on_canvas(self, event) -> None:
        for i, quad in enumerate(self.grid[1]):
            if quad[0][0] <= event.x <= quad[2][0] and quad[0][1] <= event.y <= quad[2][1]:
                sign = self.signs[i]
                sign["sign"] = not sign["sign"]
                break
        self.update_canvas()

    def update_canvas(self) -> None:
        self.background_image = self.backup_image.copy()

        if len(self.signs) == 0:
            return

        draw_img = self.background_image.copy()
        for i, quad in enumerate(self.grid[1]):
            if self.signs[i]["sign"]:
                col = (0, 255, 0)
            else:
                col = (255, 0, 0)

            cv2.rectangle(draw_img, nparray_to_point(quad[0]), nparray_to_point(quad[2]),
                          color=col,
                          thickness=-1)

        cv2.addWeighted(draw_img, 0.5, self.background_image, 0.5, 0, self.background_image)

        super(DetectSignaturesGUI, self).update_canvas()

    def cancel(self, _) -> None:
        self.master.destroy()
