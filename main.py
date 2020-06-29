import tkinter as tk
from tkinter import simpledialog

from assgui import MainGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    num_of_lectures = int(simpledialog.askstring("", "Hány előadás van ebben az évben?"))
    root.deiconify()
    gui = MainGUI(root, None, num_of_lectures)
    root.mainloop()
