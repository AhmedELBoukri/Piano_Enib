# -*- coding: utf-8 -*-
import os
from tkinter import *
from observer import Observer
import sqlite3
from observer import *
from audio import *
import subprocess
from audio_create_notes_wav import *
import frequencies_MVC
import piano_MVC


class Audio(Subject) : #Model
    def __init__(self) :
        Subject.__init__(self)

    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
        except Error as e:
            print(e)
 
        return conn   

    def Freq_val(self,note,octave) :
        conn = self.create_connection("frequencies.db")
        cur = conn.cursor()
        if "#" in note:
                note = note.replace("#","Sharp")
        cur.execute("SELECT "+ note +" FROM frequencies where octave="+octave)
        result = [row[0] for row in cur.fetchall()]
        return result[0]

    def Notes_name(self):
        Notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
        return Notes

    def Octave_name(self):
        Octaves = ["1","2","3"]
        return Octaves

    def get_freq(self) :
        return self.freq

    def get_degree(self) :
        return self.degree

    def notify(self,note,octave) :
        for obs in self.observers:
            obs.update(self,note,octave)


class Screen_audio(Observer):#View
    def __init__(self,parent) :
        #self.screen1=Frame(parent,borderwidth=9,width=300,height=150,bg="yellow")
        self.x = 1

        

    def get_screen(self) :
        return self.screen

    def update(self,model,note,octave) :  
        pass

    def packing(self) :
        #self.screen1.place(x=200,y=300)
        pass


class Controller : #controller
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.frame_1 = self.create_notes()
        self.buttons = self.create_buttons()
        self.oscillo = self.oscillo()
        self.piano = self.add_piano()


    def packing(self) :
        self.frame_1.place(relx=0.3,rely=0.01,anchor=N)
        self.buttons.place(relx=0.3,rely=0.28,anchor=N)
        self.oscillo.place(relx=0.99,rely=0.01,anchor=NE)
        self.piano.place(relx=0.5,rely=1,anchor=S)


    def create_notes(self):
        frame_1 = Frame(self.parent, borderwidth=5, pady=10)#, bg="red")
        self.var_note = StringVar(frame_1)
        self.var_octave = StringVar(frame_1)
        self.duree = DoubleVar()
        list_notes = model.Notes_name()
        list_octaves = model.Octave_name()

        #Labels
        Label(frame_1, text="Notes", font=('Arial', 10)).grid(row = 0, column = 0)
        Label(frame_1, text="Octave", font=('Arial', 10)).grid(row = 0, column = 1)

        #Dropdown notes
        self.var_note.set(list_notes[0])
        #w = apply(OptionMenu, (frame_1, self.var_note) + tuple(list_notes))
        #w.grid(row = 1, column = 0)
        #w.place(relx=0,rely=0,anchor=NW)

        #Dropdown octaves
        self.var_octave.set(list_octaves[2])
        #w = apply(OptionMenu, (frame_1, self.var_octave) + tuple(list_octaves))
        #w.grid(row = 1, column = 1)
        #w.place(relx=0.2, rely=0.2)

        #Boutton Generate
        self.b_g = Button(frame_1,text='Générer')
        #self.b_g.bind("<Button-1>", lambda event, x=Sounds_list: self.touche(x))
        self.b_g.grid(row=1,column=2)
        #b_g.place(relx=0.3,rely=0.3)

        #Boutton scrole duree
        s1 = Scale(frame_1, from_=1, to=8,
                    length=400,
                    resolution=0.5,
                    label='Duree',
                    orient=HORIZONTAL,
                    variable=self.duree)
        s1.grid(row=4,column=0,rowspan=1, columnspan=4)
        #s1.place(relx=0, rely=0, anchor=NE)


        self.info = Label(frame_1, text="Appuyez pour générer le son", font=('Arial', 10))
        self.info.grid(row=11,column=1)
        #self.info.place(relx=0, rely=0, anchor=NE)

        return frame_1

    def create_buttons(self) :
        frame_notes = Frame(self.parent,borderwidth=5,pady=10)#,bg="blue")

        #liste des fichiers note
        yDefilB = Scrollbar(frame_notes, orient='vertical')
        yDefilB.grid(row=0, column=1, sticky='ns')

        Sounds_list = Listbox(frame_notes, yscrollcommand=yDefilB.set)
        Sounds_list.grid(row=0, column=0, sticky='nsew')
        yDefilB['command'] = Sounds_list.yview

        #Boutton transfer 1
        b_switch = Button(frame_notes,text='->')
        b_switch.bind("<Button-1>",lambda event,w = Sounds_list: self.accords_list(w,Accords_list,accords_tab,Acc_list))
        b_switch.grid(row=0,column=2,padx=20, pady=20)

        #liste des notes selectioné
        Accords_list = Listbox(frame_notes)
        Accords_list.grid(row=0, column=3, sticky='nsew')

        #Boutton transfer 2
        b_switch2 = Button(frame_notes,text='->')
        b_switch2.bind("<Button-1>",lambda event,w = Sounds_list: self.generate_accord(accords_tab,Acc_list,Accords_list))
        b_switch2.grid(row=0,column=4,padx=20, pady=20)

        #liste accords
        yDefilBpp = Scrollbar(frame_notes, orient='vertical')
        yDefilBpp.grid(row=0, column=6, sticky='ns')

        Acc_list = Listbox(frame_notes, yscrollcommand=yDefilBpp.set)
        Acc_list.grid(row=0, column=5, sticky='nsew')
        yDefilBpp['command'] = Acc_list.yview

        self.sound_list(Sounds_list)
        self.accords_affich(Acc_list)

        accords_tab = []

        #Boutton play sound
        b_s = Button(frame_notes,text='Ecouter')
        b_s.bind("<Button-1>",lambda event,y = Sounds_list: self.listen_sound(y,Acc_list))
        b_s.grid(row=1,column=2,padx=5, pady=15)
        #b_s.place(relx=0.3,rely=1)

        #Boutton deletefile de la boxlist
        b_d = Button(frame_notes,text='Supprimer')
        b_d.bind("<Button-1>",lambda event,z = Sounds_list: self.delete_sound(z,Acc_list))
        b_d.grid(row=1,column=3,padx=5, pady=15)
        #b_d.place(relx=0.5,rely=0.9)

        #Boutton stop playing sound
        b_stop = Button(frame_notes,text='Visualiser')
        b_stop.bind("<Button-1>",lambda event,w = Sounds_list: self.visualiser_sound(w))
        b_stop.grid(row=1,column=4,padx=5, pady=15)
        #b_stop.place(relx=0.5,rely=0.9)


        self.b_g.bind("<Button-1>", lambda event, x=Sounds_list: self.touche(x))

        return frame_notes

    def oscillo(self):
        frame_oscillo = Frame(self.parent, borderwidth=10)#, bg="green")
        self.oscillo_model,self.oscillo_view,self.oscillo_ctrl =  frequencies_MVC.afficher_oscillo(frame_oscillo,0)
        return frame_oscillo

    def add_piano(self):
        frame_piano = Frame(self.parent,borderwidth=10,pady=10,bg="yellow")
        piano_MVC.piano_integrate(frame_piano)
        return frame_piano

    def create_wav(self,note,octave):
        NomFichier = note
        frequenceG = float(model.Freq_val(note,octave))
        frequenceD = float(model.Freq_val(note,octave))
        duree = float(self.duree.get())
        create_note_wav(octave,NomFichier,frequenceG,frequenceD,duree)

    def sound_list(self,Sounds_list):
        sound_files = os.listdir('./Sounds')
        for i in range(0,len(sound_files)):
            Sounds_list.insert(END,sound_files[i])
        print(sound_files)

        return sound_files


    def accords_list(self,Sounds_list,Accords_list,accords_tab,Acc_list):
        # accord_files = os.listdir('./Accords')
        note = Sounds_list.get(Sounds_list.curselection())
        if(len(accords_tab)<3 and note not in accords_tab):
            Accords_list.insert(END,note)
            accords_tab.append(note)
            print('------------------------')
            print(accords_tab)


    def accords_affich(self,Accords_list):
        acc_files = os.listdir('./Accords')
        for i in range(0,len(acc_files)):
            Accords_list.insert(END,acc_files[i])
        print(acc_files)

        return acc_files




        # for i in range(0,len(accord_files)):
        #     Accords_list.insert(END,accord_files[i])
        # print(accord_files)


    def generate_accord(self,accords_tab,Acc_list,Accords_list):


        data1,fech = ouvrir_wav('Sounds/'+accords_tab[0])
        data2,fech = ouvrir_wav('Sounds/'+accords_tab[1])
        data3,fech = ouvrir_wav('Sounds/'+accords_tab[2])

        note1 = accords_tab[0][:-4]
        note2 = accords_tab[1][:-4]
        note3 = accords_tab[2][:-4]

        data = [] # liste des échantillons de l'accord

        for i in range(len(data1)):
            data.append((1/3.)*(data1[i]+data2[i]+data3[i])) # calcul de la moyenne de chacun des échantillons de même index issus des trois listes


        ecrire_wav('./Accords/'+note1+'-'+note2+'-'+note3+'.wav' , data , fech)

        Acc_list.delete(0, END)
        Accords_list.delete(0, END)
        self.accords_affich(Acc_list)

        del accords_tab[:]

    #Lire la note
    def listen_sound(self,Sounds_list,Acc_list):
        if len(Sounds_list.curselection()) != 0:
            note = Sounds_list.get(Sounds_list.curselection())   #recup le nom du ficher select
            print(note)
            try:
                with open("Sounds/"+note):
                    subprocess.call(["aplay","Sounds/"+note])
            except IOError:
                print("Erreur ! fichier " + note + " introuvable sous le repertoire : "+ "Sounds/")

        else:
            note = Acc_list.get(Acc_list.curselection())   #recup le nom du ficher select
            print(note)
            try:
                with open("Accords/"+note):
                    subprocess.call(["aplay","Accords/"+note])
            except IOError:
                print("Erreur ! fichier " + note + " introuvable sous le repertoire : "+ "Accords/")


    def visualiser_sound(self,Sounds_list):
        try:
            note = Sounds_list.get(Sounds_list.curselection())   #recup le nom du ficher select
            if ("#" in note):
                self.oscillo_ctrl.update_frequency(float(self.model.Freq_val(note[0]+"Sharp", note[2])))
            else:
                self.oscillo_ctrl.update_frequency(float(self.model.Freq_val(note[0], note[1])))
        except (UnboundLocalError,TclError):
            print("note only")

    def touche(self,Sounds_list) :
        self.model.notify(self.var_note.get(),self.var_octave.get())
        self.create_wav(self.var_note.get(),self.var_octave.get())
        Sounds_list.delete(0, END)
        self.sound_list(Sounds_list)
        self.info.config(text = "Vous avez généré la note : " + self.var_note.get() + " de l'octave: " + self.var_octave.get() )

        

    def delete_sound(self,Sounds_list,Acc_list):
        try:
            note= Sounds_list.get(Sounds_list.curselection())   #recup le nom du ficher select
            Sounds_list.delete(0, END)
            print(note)
            os.remove('./Sounds/'+note)
            self.sound_list(Sounds_list)

        except TclError as Vide:
                note =  Acc_list.get(Acc_list.curselection())
                Acc_list.delete(0, END)
                print(note)
                os.remove('./Accords/'+note)
                self.accords_affich(Acc_list)
            # tkinter.messagebox.showinfo("Error ! ","Selectione un fichier son")
                pass


    def get_buttons(self) :
        return self.buttons

    def get_degrees(self) :
        return self.degrees

    


if __name__ == "__main__" :
    root = Tk()
    root.geometry("1000x650")
    root.title("Creation de son")
    model=Audio()
    controller=Controller(root,model)
    view=Screen_audio(root)
    model.attach(view)
    controller.packing()
    view.packing()
    root.mainloop()
    
