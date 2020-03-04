# -*- coding: utf-8 -*-
# http://izeunetit.fr/ICN1ere/correction/correction_son_5.html

from audio import *

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

'''data1,fech = ouvrir_wav('Sounds/C3.wav')
data2,fech = ouvrir_wav('Sounds/E3.wav')
data3,fech = ouvrir_wav('Sounds/G3.wav')

data = [] # liste des échantillons de l'accord

for i in range(len(data1)):
    data.append((1/3.)*(data1[i]+data2[i]+data3[i])) # calcul de la moyenne de chacun des échantillons de même index issus des trois listes   

ecrire_wav('C_chord.wav' , data , fech)
'''

def accord(note):
    f1 = note[0] # fréquence de la première note
    f2 = note[1] # fréquence de la deuxième
    f3 = note[2] # et de la troisième...
    data1 = wav_sinus('note1.wav' , f = f1 , fech = 8000 ,  duree = 1)
    data2 = wav_sinus('note2.wav' , f = f2 , fech = 8000 ,  duree = 1)
    data3 = wav_sinus('note3.wav' , f = f3 , fech = 8000 ,  duree = 1)


    data = []

    for i in range(len(data1)):
    	data.append((1/3.)*(data1[i]+data2[i]+data3[i]))
   
    return data

chords = {'Do':(130.81,164.81,196.00),'Mim':(164.81,196.00,246.94),'Fa':(174.61,220.00,261.63),'Rém':(146.83,174.61,220.00)}


#song = ['Do','Do','Mim','Mim','Fa','Fa','Rém','Rém','Do','Do','Mim','Mim','Fa','Fa','Rém','Rém']

song = ['Do']

data = [] # liste des échantillons de la "chanson" entière

for i in song :

	note = chords[i] # la variable note contiendra donc le tuple associé à la clé dont le nom est dans la variable i

	data_accord = accord(note) # appel de la fonction accord(), à laquelle on passe comme paramètre le tuple des 3 fréquences; data_accord contiendra la liste des échantillons de l’accord retournée par la fonction   
    
	data.extend(data_accord) # ajout à la suite des échantillons de la "chanson" de la liste des échantillons de l'accord nouvellement crée

ecrire_wav('accord.wav' , data , 8000 )	# écriture du fichier son résultant


