import json
import os
from pprint import pprint
import sqlite3
import numpy as np

db = sqlite3.connect('data/trumpdb')
cursor = db.cursor()

testString = "tell black lady husband knew signed"

cLike=np.empty(0)
cDislike=np.empty(0)
cNeutral=np.empty(0)
cIrrelevant=np.empty(0)

for word in testString.split():
    cursor.execute('''SELECT plike FROM wordsp WHERE word = ?''', (word,))
    plike = cursor.fetchall()[0][0]
    cLike = np.append(cLike,[plike])
    cursor.execute('''SELECT pdislike FROM wordsp WHERE word = ?''', (word,))
    pdislike = cursor.fetchall()[0][0]
    cDislike = np.append(cDislike, [pdislike])
    cursor.execute('''SELECT pneutral FROM wordsp WHERE word = ?''', (word,))
    pneutral = cursor.fetchall()[0][0]
    cNeutral = np.append(cNeutral,[pneutral])
    cursor.execute('''SELECT pirrelevant FROM wordsp WHERE word = ?''', (word,))
    pirrelevant = cursor.fetchall()[0][0]
    cIrrelevant = np.append(cIrrelevant,[pirrelevant])

cLike = np.prod(cLike)
cDislike = np.prod(cDislike)
cNeutral = np.prod(cNeutral)
cIrrelevant = np.prod(cIrrelevant)

chances = np.array([cLike, cDislike, cNeutral, cIrrelevant])
max = chances.max()
if max == cLike:
    print("Liked")
elif max == cDislike:
    print("Disliked")
elif max == cNeutral:
    print("Neutral")
elif max == cIrrelevant:
    print("Irrelevan")
else:
    print("Something is seriously wrong!")

print(cLike)
print(cDislike)
print(cNeutral)
print(cIrrelevant)

