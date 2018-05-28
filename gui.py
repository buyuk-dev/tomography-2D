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

        myfig = matplotlib.pyplot.figure()
        myfig.add_subplot(2, 2, 1)
        matplotlib.pyplot.title(path)
        matplotlib.pyplot.imshow(original, cmap='gray')

        myfig.add_subplot(2,2,2)
        matplotlib.pyplot.title('reconstruction')
        matplotlib.pyplot.imshow(rec, cmap='gray')

        myfig.add_subplot(2,2,3)
        matplotlib.pyplot.title('sinogram')
        matplotlib.pyplot.imshow(sinogram, cmap='gray')

        myfig.add_subplot(2,2,4)
        matplotlib.pyplot.title('filtered sinogram') 
        matplotlib.pyplot.imshow(filtered, cmap='gray')

        self.figure = gui_utils.draw_figure(self.canvas, myfig)
        
    def run(self):
        tkinter.mainloop()


app = GuiApp()
app.run()
