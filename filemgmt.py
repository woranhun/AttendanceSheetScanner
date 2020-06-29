import os
from datetime import datetime

import pdf2image


class FileMGMT:
    parent = ""

    @staticmethod
    def create_dirs(parent=""):
        FileMGMT.parent = parent
        if not os.path.exists(os.path.join(FileMGMT.parent, "output")):
            os.mkdir(os.path.join(FileMGMT.parent, "output"))

    @staticmethod
    def convert_pdf_to_img(file):
        images = pdf2image.convert_from_path(pdf_path=file, fmt="png")
        for img in images:
            img.thumbnail((1000, 1000))
        return images

    @staticmethod
    def save_to_csv(obj, num_of_lectures, path=None):
        if path is None:
            path = os.path.join(FileMGMT.parent, "output")
        file = os.path.join(path, str(datetime.now()) + ".csv")
        with open(file, "w") as file:
            file.write("Neptun;")
            file.write(";".join([f"{i}.EA" for i in range(1, num_of_lectures + 1)]))
            file.write("\n")
            for name in obj:
                file.write(str(obj[name]))
                file.write("\n")
