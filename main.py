import tkinter as tk
from typing import Tuple

import cv2
import numpy as np

from assgui import mainGUI

Point = np.ndarray
Quad = Tuple[Point, Point, Point, Point]
Line = Tuple[Point, Point]

if __name__ == "__main__":
    img = cv2.imread('testimg/10.png')
    root = tk.Tk()
    gui = mainGUI(root, img)
    root.mainloop()
