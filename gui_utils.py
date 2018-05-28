import tkinter
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()

    x,y,w,h = figure.bbox.bounds
    w, h = int(w), int(h)
    photo = tkinter.PhotoImage(master=canvas, width=w, height=h)

    canvas.create_image(loc[0] + w // 2, loc[1] + h // 2, image=photo)
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    return photo

