# -*- coding: utf-8 -*-
from math import sin,pi
import io    
from PIL import Image
## python 2.7
from Tkinter import Tk,Canvas,Scale,Button,Radiobutton,LabelFrame,IntVar,DoubleVar
import tkFileDialog

## python 3
##from tkintert Tk,Canvas,LabelFrame,Scale
##from tkinter import filedialog

from frequencies_model import Generator
from frequencies_view import Screen

class Controller :
    def __init__(self,model,view):
        self.model=model
        self.view=view
        self.view.magnitude.bind("<B2-Motion>",
                                  self.update_magnitude)
    def update_magnitude(self,event):
        x=float(event.widget.get())
        self.model.set_magnitude(x)
        self.model.generate_signal()


if __name__ == "__main__" :
   root=Tk()
   model=Generator()
   view=Screen(root,model)
   view.grid()
   model.attach(view)
   view.update(model)
   ctrl=Controller(model,view)
   view.layout()
   root.mainloop()
   
