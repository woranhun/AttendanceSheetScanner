import tkinter as tk

import cv2

from assgui import MainGUI

if __name__ == "__main__":
    img = cv2.imread('testimg/12.jpg')
    root = tk.Tk()
    gui = MainGUI(root, img)
    root.mainloop()
