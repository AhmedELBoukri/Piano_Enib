# -*- coding: utf-8 -*-
from math import sin,pi
import io    
#from PIL import Image
## python 2.7
from tkinter import Tk,Canvas,Scale,Button,Radiobutton,LabelFrame,IntVar,DoubleVar
#import tkFileDialog

## python 3
# from tkintert Tk,Canvas,LabelFrame,Scale
##
from tkinter import filedialog

from observer import *

class Generator(Subject) :
    def __init__(self,fr):
        Subject.__init__(self)
        self.signal=[]
        self.a,self.f,self.p=1,fr,0.0
        self.generate_signal()
    def get_signal(self):
        return self.signal
    def get_magnitude(self,a):
        return self.a
    def set_magnitude(self,a):
        self.a=a
        self.generate_signal()
    def set_signal(self,signal):
        self.signal=signal
        self.notify()
    def generate_signal(self):
        del self.signal[0:]
        samples=1000
        for t in range(0, samples,5):
            samples=float(samples)
            e=self.a*sin((2*pi*self.f*(t*1.0/samples))
                         -self.p)
            self.signal.append((t*1.0/samples,e))
        self.notify()
        return self.signal

class Controller :
    def __init__(self,model,view):
        self.model=model
        self.view=view
        self.view.magnitude.bind("<B1-Motion>", self.update_magnitude)
    def update_magnitude(self,event):
        x=float(event.widget.get())
        self.model.set_magnitude(x)
        self.model.generate_signal()

    def update_frequency(self,fr):
        self.model.f = fr
        self.model.generate_signal()


class Screen(Observer):
    def __init__(self,parent,model,grid_steps=10,bg="white"):
        self.parent = parent
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
        self.save_button=Button(parent,text="save",command=self.save)
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
        #print("save")
        filename = tkFileDialog.asksaveasfilename(parent=self.parent,filetypes=formats,title="Sauvez l'image sous...")
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

#if __name__ == "__main__" :
def afficher_oscillo(parent,fr):
   #root=Tk()
   model=Generator(fr)
   view=Screen(parent,model)
   view.grid()
   model.attach(view)
   view.update(model)
   ctrl=Controller(model,view)
   view.layout()
   return model,view,ctrl
   #root.mainloop()


