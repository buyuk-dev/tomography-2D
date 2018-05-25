import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()

    x,y,w,h = figure.bbox.bounds
    w, h = int(w), int(h)
    photo = tk.PhotoImage(master=canvas, width=w, height=h)

    canvas.create_image(loc[0] + w // 2, loc[1] + h // 2, image=photo)
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    return photo


w, h = 640, 480
window = tk.Tk()
window.title("A figure in a canvas")


canvas = tk.Canvas(window, width=w, height=h)
canvas.pack()


# my code starts
myfig = plt.figure()
plt.plot([x*x for x in range(100)])
fig_pic = draw_figure(canvas, myfig)
# my code ends

btn = tk.Button(window, text="click", command=window.destroy)
btn.pack()

tk.mainloop()


