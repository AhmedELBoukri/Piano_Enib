# -*- coding: utf-8 -*-

from Tkinter import Tk,Frame,Button
from piano_model import Octave
##from piano_view import Screen

class Keyboard :
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.keyboard=self.create_keyboard()
        
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        frame=Frame(self.parent,borderwidth=5,width=7*key_w,height=key_h,bg="red")
        for key in self.model.notes.keys() :
            if  key.startswith( '#',1,len(key)) :                          # black keys
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=Button(frame,name=key.lower(),width=3,height=6, bg = "black")
                button.bind("<Button-1>",lambda event,x = key : self.touche(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :                                                         # white keys
                button=Button(frame,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x = key : self.touche(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
        return frame

    def touche(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees
    def packing(self) :
        self.keyboard.pack(fill="x")

if __name__ == "__main__" :
    root = Tk()
    root.geometry("360x300")
    root.title("La leçon de piano")
    model=Octave()
    controller=Keyboard(root,model)
##    view=Screen(root)
##    model.attach(view)
##    view.packing()
    controller.packing()
    root.mainloop()
