# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
connect = sqlite3.connect("frequencies.db")
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS frequencies")
cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,\
                    CSharp float,\
                    D  float,\
                    DSharp float,\
                    E float,\
                    F float,\
                    FSharp float,\
                    G float,\
                    GSharp float,\
                    A      float,\
                    ASharp float,\
                    B float\
);")


f0=[110, 220, 440]
frequencies=[]
insert=[]
octave=[1,2,3]
#octave.append(3)
for i in range(0,len(octave)):
    insert.append(octave[i])
    for j in range (-9,3) :     # les frequences des 12 notes de la gamme de degre 3 referencees par rapport au LA (A) 440 Hz
        frequency=f0[i]*2**(j/12.)
        insert.append(frequency)
    frequencies.append(insert)
    cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)
    connect.commit()
    del insert[:]
    del frequencies[:]
