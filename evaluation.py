import json
import os
from pprint import pprint
import sqlite3
import numpy as np
import time
t0=time.time()

db = sqlite3.connect('data/thdb')
cursor = db.cursor()

punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’…—'
stopWordsNoP = ["rt","a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"]

def stopWordRemover (text, swords):
    return list(set([word for word in text.split() if word.lower() not in swords]))

def linkRemover (text):
    #return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('@') or word.lower().startswith('http'))]))
    return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('http'))]))


cursor.execute('''SELECT tweet, class FROM tweetsTest''')
testSet = cursor.fetchall()

trueHillary = 0
falseHillary = 0
trueTrump = 0
falseTrump = 0

for row in testSet:
    tweet = row[0]
    tweetNP = tweet.translate(str.maketrans("", "", punc))
    tweetNPSW = ' '.join(stopWordRemover(tweetNP, stopWordsNoP))
    testString = ' '.join(linkRemover(tweetNPSW))
    #print(testString)

    #testString = "timobrien wviolating democratshill campaign lawsthen guilty helping finance"
    cHil = np.empty(0)
    cTru = np.empty(0)
    #cNeutral = np.empty(0)
    #cIrrelevant = np.empty(0)

    for word in testString.split():
        w = cursor.execute("SELECT EXISTS(SELECT 1 FROM wordsp WHERE word = ?)", (word,))
        if w.fetchone()[0]:
            # cursor.execute('''INSERT OR IGNORE INTO wordsp(word) VALUES(?)''', (word,))
            cursor.execute('''SELECT phil FROM wordsp WHERE word = ?''', (word,))
            phil = cursor.fetchall()[0][0]
            cHil = np.append(cHil, [phil])
            cursor.execute('''SELECT ptru FROM wordsp WHERE word = ?''', (word,))
            ptru = cursor.fetchall()[0][0]
            cTru = np.append(cTru, [ptru])
            # cursor.execute('''SELECT pneutral FROM wordsp WHERE word = ?''', (word,))
            # pneutral = cursor.fetchall()[0][0]
            # cNeutral = np.append(cNeutral, [pneutral])
            # cursor.execute('''SELECT pirrelevant FROM wordsp WHERE word = ?''', (word,))
            # pirrelevant = cursor.fetchall()[0][0]
            # cIrrelevant = np.append(cIrrelevant, [pirrelevant])

    cHil = np.prod(cHil)
    cTru = np.prod(cTru)
    # cNeutral = np.prod(cNeutral)
    # cIrrelevant = np.prod(cIrrelevant)

    chances = np.array([cHil, cTru])#, cNeutral, cIrrelevant])
    max = chances.max()
    if max == cHil:
        # print("Model states Hillary")
        # print("Label was "+str(row[1]))
        if str(row[1]) == "HillaryClinton":
            trueHillary +=1
        elif str(row[1]) == "realDonaldTrump":
            falseHillary +=1
    elif max == cTru:
        # print("Model states Trump")
        # print("Label was "+str(row[1]))
        if str(row[1]) == "realDonaldTrump":
            trueTrump += 1
        elif str(row[1]) == "HillaryClinton":
            falseTrump += 1
    # elif max == cNeutral:
    #     print("Model states Neutral")
    #     print("Label was "+str(row[1]))
    # elif max == cIrrelevant:
    #     print("Model states Irrelevant")
    #     print("Label was "+str(row[1]))
    else:
        print("Something is seriously wrong!")
        print("Label was "+str(row[1]))

    #print(cHil)
    #print(cTru)

    # print(cNeutral)
    # print(cIrrelevant)

print("trueHillary = "+str(trueHillary))
print("falseHillary = "+str(falseHillary))
print("trueTrump = "+str(trueTrump))
print("falseTrump = "+str(falseTrump))

accuracy = (trueHillary+trueTrump)/(trueHillary+trueTrump+falseHillary+falseTrump)
print(accuracy)

db.close()

t1 = time.time()
print("Total time: "+str(t1-t0))