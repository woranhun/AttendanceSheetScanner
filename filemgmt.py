import os
from datetime import datetime

import pdf2image


class FileMGMT:
    parent = ""

    @staticmethod
    def createDirs(parent=""):
        FileMGMT.parent = parent
        if not os.path.exists(os.path.join(FileMGMT.parent, "src")):
            os.mkdir(os.path.join(FileMGMT.parent, "src"))
        if not os.path.exists(os.path.join(FileMGMT.parent, "src", "pdf")):
            os.mkdir(os.path.join(FileMGMT.parent, "src", "pdf"))
        if not os.path.exists(os.path.join(FileMGMT.parent, "src", "img")):
            os.mkdir(os.path.join(FileMGMT.parent, "src", "img"))
        if not os.path.exists(os.path.join(FileMGMT.parent, "src", "csv")):
            os.mkdir(os.path.join(FileMGMT.parent, "src", "csv"))

    @staticmethod
    def convertPDFToIMG(file):
        dst = os.path.join(FileMGMT.parent, "src", "img", str(datetime.now().date()) + "_" + str(datetime.now().hour))
        if not os.path.exists(dst):
            os.mkdir(dst)
        pdf2image.convert_from_path(pdf_path=file, output_folder=dst, fmt="png")
        print(dst)

    @staticmethod
    def saveToCSV(ou, numOfLectures=14, path=None):
        if path is None:
            path = os.path.join(FileMGMT.parent, "src", "csv")
        file = os.path.join(path, str(datetime.now().date()) + "_" + str(datetime.now().hour) + ".csv")
        with open(file, "w") as file:
            file.write("Neptun;")
            file.write(";".join([str(i) + ".EA" for i in range(1, numOfLectures + 1)]))
            file.write("\n")
            for student in ou:
                file.write(";".join(student))
                file.write("\n")