import matplotlib.pyplot
import numpy as np
import tkinter
import tkinter.ttk
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

        self.btn = tkinter.Button(text="scan", higcommand=lambda: self.on_scan())
        self.btn.pack()

        self.progress_bar = tkinter.ttk.Progressbar(orient=tkinter.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tkinter.X)
        self.progress = 0

        self.path_entry = tkinter.Entry(width=50)
        self.path_entry.insert(0, "image path")
        self.path_entry.pack()

        self.frame_params = tkinter.Frame()
        self.frame_params.pack()

        self.sampling_entry = tkinter.Entry(self.frame_params, width=10)
        self.sampling_entry.insert(0, "sampling")
        self.sampling_entry.pack(side=tkinter.LEFT)

        self.resolution_entry = tkinter.Entry(self.frame_params, width=10)
        self.resolution_entry.insert(0, "resolution")
        self.resolution_entry.pack(side=tkinter.LEFT)

        self.span_entry = tkinter.Entry(self.frame_params, width=10)
        self.span_entry.insert(0, "span")
        self.span_entry.pack(side=tkinter.LEFT)
        
        self.rms_label = tkinter.Label(text="RMS: N/A", width=20)
        self.rms_label.pack()


    def increment_progress(self):
        self.progress_bar.step(10)
        if self.progress_bar['value'] == self.progress_bar['maximum']:
            print("scanning completed")

    def on_scan(self):
        path = self.path_entry.get()
        self.path_entry.delete(0, tkinter.END)

        original, sinogram, filtered, rec = main.main(path, lambda: self.increment_progress())

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
