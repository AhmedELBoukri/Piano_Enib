# -*- coding: utf-8 -*-

from Tkinter import Tk,Frame,Label
from piano_model import Octave
from piano_controller import Keyboard
import subprocess
from observer import Observer

class Screen(Observer):
    def __init__(self,parent) :
        self.screen=Frame(parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=Label(self.screen,text="Appuyez sur une touche clavier ", bg="pink",font=('Arial',10))
    def get_screen(self) :
        return self.screen
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.notes.keys()  :
                raise AssertionError    
        subprocess.call(["aplay", model.get_notes()[key]])
        if self.info :
            self.info.config(text = "Vous avez joue la note : " + key + str(model.get_degree()))
    def packing(self) :
        self.screen.pack()
        self.info.pack()

if __name__ == "__main__" :
    root = Tk()
    root.geometry("360x300")
    root.title("La leçon de piano")
    model=Octave()
##    controller=Keyboard(root,model)
    view=Screen(root)
    model.attach(view)
##    controller.packing()
    view.packing()
    root.mainloop()
