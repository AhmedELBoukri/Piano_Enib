#!/usr/bin/env python
#-*- coding: utf-8 -*-

# http://izeunetit.fr/ICN1ere/correction/correction_son_5.html

# script audio.py
# (C) Fabrice Sincère ; Jean-Claude Meilland ...
# RESTRICTIONS : PCM mono 16 bits signés ( -32 767 -> + 32 767 )

# http://blog.acipo.com/wave-generation-in-python/
# https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
# https://www.programcreek.com/python/example/82393/wave.open
import wave
import struct
import binascii
##    elif (fichier.getsampwidth() != 2): # test profondeur encodage
##        print('Le fichier son doit être encodé sur 16 bits. (Ici: '+str(8*fichier.getsampwidth())+' bits.)')
##                
##    else :

    # construction de la liste des échantillons
    for i in range( fichier.getnframes() ): # parcours de la suite des échantillons ( getnframes() = nombre total d'échantillons )
    
        valeur = fichier.readframes(1) # lecture d'un échantillon et passage au suivant
        data.append(struct.unpack("=h",valeur)[0]) # formule auto-magique pour le décodage...
                        
    fichier.close()

    return data, fech


''' écriture d'un fichier WAV 16 bits mono
    data = liste des échantillons entiers sur 16 bits non-signés ( valeurs inférieures à - 32 767 et supérieures à + 32 767 ramenées à leurs limites respectives )
    fech = fréquence d'échantillonnage : 8000, 11025, 22050, 41 000, 44100 et éventuellement 48000 et 96000
'''
def ecrire_wav(nom_fichier , data , fech ):
    
    fichier = wave.open(nom_fichier,'w')

    # création en-tête
    nbCanal = 1    # mono
    nbOctet = 2    # taille d'un échantillon : 2 octets = 16 bits
    nbEchantillon = len(data) # nombre total d'échantillon

    parametres = (nbCanal,nbOctet,fech,nbEchantillon,'NONE','not compressed')# tuple
    fichier.setparams(parametres)    # création de l'en-tête (44 octets)

    # écriture des données
    print('Veuillez patienter...')
    
    for i in range(0,nbEchantillon):
        
        data[i] = int(data[i]) # au cas où une valeur non entière traînerait...

        # écrétage si valeur en dehors de l'intervalle [-32767,+32767]
        if ( data[i] < -32767 ):
            data[i] = -32767
        elif ( data[i] > 32767 ): 
            data[i] = 32767 
                   
        fichier.writeframes(wave.struct.pack('h',data[i])) # codage et écriture échantillon 16 bits signés

    print("Écriture fichier WAV: '"+nom_fichier+"' terminée.")

    fichier.close()



''' crée un fichier WAV d'onde sinusoïdale
    f = fréquence du son ( par défaut = 440 Hz )
    fech = fréquence d'échantillonnage : 11025, 22050, 44100 et éventuellement 48000 et 96000 ( par défaut = 8000 Hz )
    duree = durée du son en s ( par défaut = 2s )
'''
def wav_sinus( nom_fichier = 'sinus.wav' , f = 440 , fech = 8000 , duree = 2 ):
        
    data = [int(30000*math.cos(2*math.pi*f*i/fech)) for i in range(int(fech*duree))] # fech*duree = nombre total d'échantillons

    ecrire_wav(nom_fichier, data , fech)

    return data



''' crée un fichier WAV d'onde triangle
    f = fréquence du son ( par défaut = 440 Hz )
    fech = fréquence d'échantillonnage : 11025, 22050, 44100 et éventuellement 48000 et 96000 ( par défaut = 8000 Hz )
    duree = durée du son en s ( par défaut = 2s )
'''
def wav_triangle( nom_fichier = 'triangle.wav' , f = 440 , fech = 8000 , duree = 2 ):

    data = [int(30000*(2/math.pi)*math.asin(math.sin(2*math.pi*f*i/fech))) for i in range(int(fech*duree))] # fech*duree = nombre total d'échantillons

    ecrire_wav(nom_fichier, data , fech)

    return data

''' crée un fichier WAV d'onde carrée
    f = fréquence du son ( par défaut = 440 Hz )
    fech = fréquence d'échantillonnage : 11025, 22050, 44100 et éventuellement 48000 et 96000 ( par défaut = 8000 Hz )
    duree = durée du son en s ( par défaut = 2s )
'''
def wav_carre( nom_fichier = 'carre.wav' , f = 440 , fech = 8000 , duree = 2 ):

    data = []
    
    for i in range(int(fech*duree)): # fech*duree = nombre total d'échantillons

        valeur = int(30000*math.cos(2*math.pi*f*i/fech))
    
        data.append( 30000*(valeur / math.fabs(valeur or 1)) )

    ecrire_wav(nom_fichier, data , fech)

    return data

    

''' créée un fichier WAV de bruit blanc ( = valeurs d'échantillons au hasard )
    fech = fréquence d'échantillonage : 11025, 22050, 44100 et éventuellement 48000 et 96000 ( par défaut = 8000 Hz )
    duree = durée du son en s  ( par défaut = 2s )
'''
def wav_blanc( nom_fichier = 'blanc.wav' , fech = 8000 , duree = 2 ):

    data = [random.randint(-32767,32767) for i in range(int(fech*duree))] # fech*duree = nombre total d'échantillons

    ecrire_wav(nom_fichier, data , fech)

    return data




