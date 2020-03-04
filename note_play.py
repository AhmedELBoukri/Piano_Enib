# -*- coding: utf-8 -*-
import subprocess

if __name__ == "__main__" :
    notes=("A","B","C","D","E","F","G")
    octaves=[1,2,3]
    print("Choisissez une  note parmi : ",notes)
    note=raw_input("Note a jouer :")
    while note not in notes :
        print("Choisissez une  note parmi : ",notes)
        note=raw_input('Note a jouer :')
    print("Choisissez une  octave parmi : ",octaves)
    octave=int(raw_input('Octave :'))
    while octave not in octaves :
        print("Choisissez une  octave parmi : ",octaves)
        octave=int(raw_input('Octave :'))
    try:
        with open("Sounds/"+note+str(octave)+".wav"):
            subprocess.call(["aplay","Sounds/"+note+str(octave)+".wav"])
    except IOError:
        print("Erreur ! fichier " + note+str(octave)+".wav" + " introuvable sous le repertoire : "+ "Sounds/")
 
