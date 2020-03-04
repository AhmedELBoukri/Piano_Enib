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

from observer import Observer
from frequencies_model import Generator
# from frequencies_controller import Controller

class Screen(Observer):
    def __init__(self,parent,model,grid_steps=10,bg="white"):
        self.model=model
        self.canvas=Canvas(parent,bg=bg)
        self.width,self.height=int(self.canvas.cget("width")),int(self.canvas.cget("height"))
        self.grid_steps=grid_steps
        self.signal_id=None
        self.signal_frame=LabelFrame(parent,text="Signal", padx=5, pady=5,fg="red")
        self.magnitude=Scale(self.signal_frame,
                             orient="horizontal",
                             label="Magnitude",
                             resolution=0.1,
                             length=250,
                             from_=0,to=2,
                             tickinterval=25)
        self.save_button=Button(text="save",command=self.save)
        self.canvas.bind("<Configure>", self.resize)
    def get_grid_steps(self,grid_steps):
        return self.grid_steps
    def set_grid_steps(self,grid_steps):
        self.grid_steps=grid_steps

    def update(self,model):
        signal=model.get_signal()
        self.plot_signal(signal)
    def plot_signal(self,signal,color="red"):
        signal_id=None
        if self.canvas.find_withtag("signal") :
            self.canvas.delete("signal")
        if signal and len(signal) > 1:
            plot=[ (x*self.width, self.height/2.0*(y+1))
                    for (x, y) in signal ]
            signal_id=self.canvas.create_line(plot,
                                         fill=color,
                                         smooth=1,
                                         width=3,
                                         tags="signal")
        return signal_id
    def grid(self):
        self.canvas.create_line(0,self.height/2,self.width,self.height/2,tags="grid")
        self.canvas.create_line(10,self.height-5,10,5,arrow="last",tags="grid")
        step=self.width/self.grid_steps
        for t in range(self.grid_steps+1):
            x =t*(step+0.6)
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=1,tags="grid")
    def resize(self, event):
        self.width = event.width
        self.height = event.height
        print(self.width,self.height)
        self.canvas.delete("grid")
        self.canvas.delete("signal")
        self.plot_signal(self.model.get_signal())
        self.grid()

    def save(self) :
        formats =[
            ('Texte','*.py'),
            ('Portable Network Graphics','*.png'),
            ('JPEG / JFIF','*.jpg'),
             ('CompuServer GIF','*.gif'),
        ]
        print("save")
        filename = tkFileDialog.asksaveasfilename(parent=root,filetypes=formats,title="Sauvez l'image sous...")
        if filename :
            ps = self.canvas.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(filename)
            img.close()

    def layout(self) :
        self.canvas.pack(expand=True,fill="both")
        self.signal_frame.pack(side="left",expand=True,fill="x")
        self.magnitude.pack(expand=True,fill="x")
        self.save_button.pack()

if __name__ == "__main__" :
   root=Tk()
   model=Generator()
   view=Screen(root,model)
   view.grid()
   model.attach(view)
   view.update(model)
#   ctrl=Controller(model,view)
   view.layout()
   root.mainloop()
   
