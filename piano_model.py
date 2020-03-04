# -*- coding: utf-8 -*-

import collections
from observer import Subject

class Octave(Subject) :
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.notes=self.create_notes()
        print("self.degree", self.degree)
    def create_notes(self) :
        folder="Sounds"
        names=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        notes=collections.OrderedDict()
        for key in names :
            notes[key]="Sounds/"+key+str(self.degree)+".wav"
        return notes
    def get_notes(self) :
        return self.notes
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

if __name__ == "__main__" :
    model=Octave()
    print(model.get_notes())
 
