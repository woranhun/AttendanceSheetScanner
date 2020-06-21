import os
from datetime import datetime

import pdf2image


class PDFToIMG:
    parent = ""

    @staticmethod
    def createDirs(parent=""):
        PDFToIMG.parent = parent
        if not os.path.exists(os.path.join(PDFToIMG.parent, "src")):
            os.mkdir(os.path.join(PDFToIMG.parent, "src"))
        if not os.path.exists(os.path.join(PDFToIMG.parent, "src", "pdf")):
            os.mkdir(os.path.join(PDFToIMG.parent, "src", "pdf"))
        if not os.path.exists(os.path.join(PDFToIMG.parent, "src", "img")):
            os.mkdir(os.path.join(PDFToIMG.parent, "src", "img"))

    @staticmethod
    def convertPDFToIMG(file):
        dst = os.path.join(PDFToIMG.parent, "src", "img",str(datetime.now().date()) +"_"+ str(datetime.now().hour))
        if not os.path.exists(dst):
            os.mkdir(dst)
        pdf2image.convert_from_path(pdf_path=file, output_folder=dst,fmt="png")
        print(dst)
