# -*- coding: utf-8 -*-

# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter
import collections

from tkinter import *
import random, time
import subprocess
from observer import *
import os

class Octave(Subject) :
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.notes=self.create_notes()
        #pygame.init()
        print("self.degree", self.degree)
    def create_notes(self) :
        ############################################
        '''sound_files = os.listdir('./Sounds')
        ###########################################
        names = []
        for file in sound_files:
            names.append(file[:len(file)-4])'''

        #folder="Sounds"
        names=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]

        names_2 = []
        for i in range(1, 4):
            for n in names:
                names_2.append( n+str(i) )

        #print names_2

        notes=collections.OrderedDict()
        for key in names_2 :
            notes[key]="Sounds/"+key+".wav"
        return notes

    def get_notes(self) :
        return self.notes
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

class Screen(Observer):
    def __init__(self,parent) :
        self.screen=Frame(parent,borderwidth=5,width=800,height=160,bg="pink")
        self.info=Label(self.screen,text="Appuyez sur une touche clavier ", bg="pink",font=('Arial',10))
    def get_screen(self) :
        return self.screen
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.notes.keys()  :
                raise AssertionError 
        #sound = pygame.mixer.Sound(model.get_notes()[key])
        #pygame.mixer.Sound.play(sound)
        try:
            with open(model.get_notes()[key]):
                subprocess.call(["aplay",model.get_notes()[key]])
        except IOError:
            print("Erreur ! fichier " + model.get_notes()[key] + " introuvable sous le repertoire : "+ "Sounds/")
	
        if self.info :
            self.info.config(text = "Vous avez joue la note : " + key)
    def packing(self) :
        self.screen.pack()
        self.info.pack()

class Keyboard :
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.keyboard=self.create_keyboard()
        
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        frame=Frame(self.parent,borderwidth=5,width=21*key_w,height=key_h,bg="red")
        #print(self.model.notes.keys())
        for key in self.model.notes.keys() :
            if  key.startswith( '#',1,len(key)) :                          # black keys
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=Button(frame,name=key.lower(),width=3,height=6, bg = "black")
                #print(key.lower())
                button.bind("<Button-1>",lambda event,x = key : self.touche(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                elif key.startswith('A#', 0, len(key)):
                        dx_black = dx_black + 2
                else :
                    dx_black=dx_black+1
            else :                                                          # white keys
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

#if __name__ == "__main__" :
def piano_integrate(root):
    '''root = Tk()
    root.geometry("900x300")
    root.title("La leçon de piano")'''
    model=Octave()
    controller=Keyboard(root,model)
    view=Screen(root)
    model.attach(view)
    controller.packing()
    view.packing()
    #root.mainloop()