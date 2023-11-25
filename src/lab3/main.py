import gui
import tkinter as tk


def main():
    root = tk.Tk()
    app = gui.GUI(root)
    app.create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
