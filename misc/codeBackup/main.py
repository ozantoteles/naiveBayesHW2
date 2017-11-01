import json
import os
from pprint import pprint
import sqlite3
import numpy as np

db = sqlite3.connect('data/trumpdb')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tweetsTest(id INTEGER PRIMARY KEY, tid INT, tweet TEXT, tweetNP TEXT, tweetNPSW TEXT, class TEXT)''')

db.commit()

punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’…'
stopWordsNoP = ["rt","a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"]

def stopWordRemover (text, swords):
    return list(set([word for word in text.split() if word.lower() not in swords]))

def linkRemover (text):
    #return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('@') or word.lower().startswith('http'))]))
    return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('http'))]))

for jsonFilename in os.listdir('dumpTest'):
    with open("dumpTest\\"+jsonFilename) as json_file:
        data = json.load(json_file)
        tid = data["id"]
        tweet = data["text"].lower()
        tweetNP = tweet.translate(str.maketrans("","", punc))
        tweetNPSW = ' '.join(stopWordRemover(tweetNP, stopWordsNoP))
        tweetNPSW = ' '.join(linkRemover(tweetNPSW))
        #tweetNPSW = tweetNP ## comment this line after test
        #' '.join(item for item in s.split() if not (item.startswith('www.') and item.endswith('.com') and len(item) > 7))
        #tweetNPSW = tweet.translate(str.maketrans("", "", stopWordsNoP))
        #tweetNPSW = [i for i in tweetNP if i not in stopWordsNoP]
        #tweetNPSW = ' '.join(tweetNPSW)
        #tweetNPSW = [i for i in tweetNP if i not in stopWordsNoP]

        pprint(tid)
        pprint(tweet)

        label = input("Press l for like, d for dislike, n for neutral, i for irrelevant \n")
        if label == "l":
            classOf = "liked"
            #cursor.execute('''UPDATE words SET likeCount = likeCount + ? WHERE word = ?''', (1, word))
        elif label == "d":
            classOf = "disliked"
            #cursor.execute('''UPDATE words SET dislikeCount = dislikeCount + ? WHERE word = ?''', (1, word))
        elif label == "n":
            classOf = "neutral"
            #cursor.execute('''UPDATE words SET neutralCount = neutralCount + ? WHERE word = ?''', (1, word))
        elif label == "i":
            classOf = "irrelevant"
            #cursor.execute('''UPDATE words SET irrelevantCount = irrelevanCount + ? WHERE word = ?''', (1, word))
        else:
            classOf = "irrelevant"
            #cursor.execute('''UPDATE words SET irrelevantCount = irrelevanCount + ? WHERE word = ?''', (1, word))

        cursor.execute('''INSERT INTO tweetsTest(tid, tweet, tweetNP, tweetNPSW, class) VALUES(?,?,?,?,?)''',
                       (tid, tweet, tweetNP, tweetNPSW, classOf))

        #pprint(tweetNP)
        pprint(tweetNPSW)
        print("-------------\n\n")
        #pprint(classOf)

db.commit()



db.close()