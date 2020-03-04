# -*- coding: utf-8 -*-
from math import sin,pi

from observer import Subject

class Generator(Subject) :
    def __init__(self):
        Subject.__init__(self)
        self.signal=[]
        self.a,self.f,self.p=1.0,1.0,0.0
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

if __name__ == "__main__" :
   model=Generator()
   print(model.get_signal())
