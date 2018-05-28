import matplotlib.pyplot
import numpy as np
import tkinter
import gui_utils
import main


# Create window
w, h = 640, 480
window = tkinter.Tk()
window.title("A figure in a canvas")
window.protocol("WM_DELETE_WINDOW", window.quit)

# Create canvas
canvas = tkinter.Canvas(window, width=w, height=h)
canvas.pack()

fig_pic = None

def on_click():
    global fig_pic
    global pathEntry
    
    path = pathEntry.get()
    pathEntry.delete(0, tkinter.END)

    original, sinogram, filtered, rec = main.main(path)

    myfig = matplotlib.pyplot.figure()
    myfig.add_subplot(2, 2, 1)
    matplotlib.pyplot.title('input')
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

    fig_pic = gui_utils.draw_figure(canvas, myfig)


btn = tkinter.Button(text="scan", command=on_click)
btn.pack()

pathEntry = tkinter.Entry()
pathEntry.pack()

tkinter.mainloop()


