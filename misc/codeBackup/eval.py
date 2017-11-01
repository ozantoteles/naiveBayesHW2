import json
import os
from pprint import pprint
import sqlite3
import numpy as np

db = sqlite3.connect('data/trumpdb')
cursor = db.cursor()

punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’…'
stopWordsNoP = ["rt","a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"]

def stopWordRemover (text, swords):
    return list(set([word for word in text.split() if word.lower() not in swords]))

def linkRemover (text):
    #return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('@') or word.lower().startswith('http'))]))
    return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('http'))]))


cursor.execute('''SELECT tweet, class FROM tweetsTest''')
testSet = cursor.fetchall()

for row in testSet:
    tweet = row[0]
    tweetNP = tweet.translate(str.maketrans("", "", punc))
    tweetNPSW = ' '.join(stopWordRemover(tweetNP, stopWordsNoP))
    testString = ' '.join(linkRemover(tweetNPSW))
    print(testString)

    #testString = "timobrien wviolating democratshill campaign lawsthen guilty helping finance"
    cLike = np.empty(0)
    cDislike = np.empty(0)
    cNeutral = np.empty(0)
    cIrrelevant = np.empty(0)

    for word in testString.split():
        w = cursor.execute("SELECT EXISTS(SELECT 1 FROM wordsp WHERE word = ?)", (word,))
        if w.fetchone()[0]:
            # cursor.execute('''INSERT OR IGNORE INTO wordsp(word) VALUES(?)''', (word,))
            cursor.execute('''SELECT plike FROM wordsp WHERE word = ?''', (word,))
            plike = cursor.fetchall()[0][0]
            cLike = np.append(cLike, [plike])
            cursor.execute('''SELECT pdislike FROM wordsp WHERE word = ?''', (word,))
            pdislike = cursor.fetchall()[0][0]
            cDislike = np.append(cDislike, [pdislike])
            cursor.execute('''SELECT pneutral FROM wordsp WHERE word = ?''', (word,))
            pneutral = cursor.fetchall()[0][0]
            cNeutral = np.append(cNeutral, [pneutral])
            cursor.execute('''SELECT pirrelevant FROM wordsp WHERE word = ?''', (word,))
            pirrelevant = cursor.fetchall()[0][0]
            cIrrelevant = np.append(cIrrelevant, [pirrelevant])

    cLike = np.prod(cLike)
    cDislike = np.prod(cDislike)
    cNeutral = np.prod(cNeutral)
    cIrrelevant = np.prod(cIrrelevant)

    chances = np.array([cLike, cDislike, cNeutral, cIrrelevant])
    max = chances.max()
    if max == cLike:
        print("Model states Liked")
        print("Label was "+str(row[1]))
    elif max == cDislike:
        print("Model states Disliked")
        print("Label was "+str(row[1]))
    elif max == cNeutral:
        print("Model states Neutral")
        print("Label was "+str(row[1]))
    elif max == cIrrelevant:
        print("Model states Irrelevant")
        print("Label was "+str(row[1]))
    else:
        print("Something is seriously wrong!")
        print("Label was "+str(row[1]))

    print(cLike)
    print(cDislike)
    print(cNeutral)
    print(cIrrelevant)

