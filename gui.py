import matplotlib.pyplot
import numpy as np
import tkinter
import gui_utils
import main


class GuiApp:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Tomography 2D")
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        self.figure = None

        self.canvas = tkinter.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        self.btn = tkinter.Button(text="scan", command=lambda: self.on_scan())
        self.btn.pack()

        self.path_entry = tkinter.Entry()
        self.path_entry.pack()

    def on_scan(self):
        path = self.path_entry.get()
        self.path_entry.delete(0, tkinter.END)

        original, sinogram, filtered, rec = main.main(path)

        plotter = main.Plotter((2,2))
        plotter.plot(original, 1, path) 
        plotter.plot(rec, 2, 'reconstruction')
        plotter.plot(sinogram, 3, 'sinogram')
        plotter.plot(filtered, 4, 'filtered sinogram')
    
        self.figure = gui_utils.draw_figure(self.canvas, plotter.figure)
        
    def run(self):
        tkinter.mainloop()


if __name__ == '__main__':
    app = GuiApp()
    app.run()
