import threading
import queue
import matplotlib.pyplot
import numpy as np
import tkinter
import tkinter.ttk
import gui_utils
import main
import plotter
import os


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

        self.progress_bar = tkinter.ttk.Progressbar(orient=tkinter.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tkinter.X)
        self.progress = 0

        def select_file():
            self.filename = tkinter.filedialog.askopenfilename(
                initialdir=os.path.abspath(os.curdir),
                title='select image'
            )

        self.path_entry = tkinter.Button(text="browse", command=select_file)
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
      
        self.filter_switch_value = tkinter.StringVar() 
        self.filter_switch = tkinter.Checkbutton(
            self.frame_params, 
            text="filter",
            variable=self.filter_switch_value,
            onvalue="RAMP",
            offvalue=None
            )
        self.filter_switch.pack(side=tkinter.LEFT) 
 
        self.rms_label = tkinter.Label(text="RMS: N/A", fg="red", width=20)
        self.rms_label.pack()
 
        def poll_queue():
            if not self.data_queue.empty():
                original, sinogram, filtered, rec, rms = self.data_queue.get()
                self.rms_label['text'] = str(rms)
                plt = plotter.Plotter((2,2))
                plt.plot(original, 1, self.cfg.path.split("/")[-1]) 
                plt.plot(rec, 2, 'reconstruction')
                plt.plot(sinogram, 3, 'sinogram')
                plt.plot(filtered, 4, 'filtered sinogram')
                self.figure = gui_utils.draw_figure(self.canvas, plt.figure)
            self.root.after(100, poll_queue)

        self.root.after(100, poll_queue)

        self.data_queue = queue.Queue()

    def read_config(self):
        class Config:
            pass
        cfg = Config()
        cfg.filter = self.filter_switch_value.get()
        cfg.span = float(self.span_entry.get())
        cfg.path = self.filename
        cfg.resolution = int(self.resolution_entry.get())
        cfg.sampling = int(self.sampling_entry.get())
        self.cfg = cfg
 
    def increment_progress(self, val=10):
        self.progress_bar.step(val)
        if self.progress_bar['value'] == self.progress_bar['maximum']:
            print("scanning completed")

    def set_progress(self, val):
        self.progress_bar['value'] = int(val)

    def on_scan(self):
        def scan():
            try:
                self.read_config()
                data = main.main(self.cfg, self)
                self.data_queue.put(data)
            except Exception as e:
                print(e)
        threading.Thread(target=scan).start()
        
    def run(self):
        tkinter.mainloop()


if __name__ == '__main__':
    app = GuiApp()
    app.run()
