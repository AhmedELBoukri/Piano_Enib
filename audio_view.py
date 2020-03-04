# -*- coding: utf-8 -*-

from Tkinter import *
from piano_controller import Keyboard
import subprocess
from observer import Observer
import sqlite3
from observer import *



class Audio(Subject) :
    def __init__(self) :
        Subject.__init__(self)

        
    def Freq_val(self) :
        cur = conn.cursor()
        cur.execute("SELECT A,ASharp,B,C,CSharp,D,DSharp,E,F,FSharp,G,GSharp FROM frequencies ")
        rows = cur.fetch()
        freq = []
        for row in rows:
            freq.append(row)
        
    def get_freq(self) :
        return self.freq
    def get_degree(self) :

        for obs in self.observers:
            obs.update(self,key)


class Screen_audio(Observer):
    def __init__(self,parent) :
        self.screen=Frame(parent,borderwidth=9,width=300,height=150)
        self.info=Label(self.screen,text="Appuyez pour générer le son",font=('Arial',10))
        self.b_g = Button(self.screen,text='Générer')
        self.frame_notes = Frame(parent,borderwidth=9,pady=100)


        conn = self.create_connection("frequencies.db")
        list_notes = self.select_all_notes(conn)
        i=0
        for note in list_notes:
            Checkbutton(self.frame_notes, text=str(note),padx=5).grid(row = 1, column = i)
            i+=1
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
        self.screen.place(x=200,y=300)
        self.info.pack()
        self.b_g.pack()
        self.frame_notes.pack()

    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
        except Error as e:
            print(e)
 
        return conn

    def select_all_notes(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT A,ASharp,B,C,CSharp,D,DSharp,E,F,FSharp,G,GSharp FROM frequencies ")
        rows = cur.fetchone()
        fren = []
        for key in rows.keys():
            fren.append(key)
        return fren




if __name__ == "__main__" :
    root = Tk()
    root.geometry("700x400")
    root.title("La leçon de piano")
    model=Audio()
##    controller=Keyboard(root,model)
    view=Screen_audio(root)
    model.attach(view)
##    controller.packing()
    view.packing()
    root.mainloop()
    
