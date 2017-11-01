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
    return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('http'))]))


cursor.execute('''SELECT tweet, class FROM tweetsTest''')
testSet = cursor.fetchall()

randT = np.random.randint(0,len(testSet))
tweet = testSet[randT][0]
print("tweet:\n"+tweet)
tweetNP = tweet.translate(str.maketrans("", "", punc))
tweetNPSW = ' '.join(stopWordRemover(tweetNP, stopWordsNoP))
testString = ' '.join(linkRemover(tweetNPSW))
print("preprocessed tweet:\n"+testString)

cHil = np.empty(0)
cTru = np.empty(0)

for word in testString.split():
    w = cursor.execute("SELECT EXISTS(SELECT 1 FROM wordsp WHERE word = ?)", (word,))
    if w.fetchone()[0]:
        cursor.execute('''SELECT phil FROM wordsp WHERE word = ?''', (word,))
        phil = cursor.fetchall()[0][0]
        cHil = np.append(cHil, [phil])
        cursor.execute('''SELECT ptru FROM wordsp WHERE word = ?''', (word,))
        ptru = cursor.fetchall()[0][0]
        cTru = np.append(cTru, [ptru])

cHil = np.prod(cHil)
cTru = np.prod(cTru)

chances = np.array([cHil, cTru])
max = chances.max()
if max == cHil:
    if str(testSet[randT][1]) == "HillaryClinton":
        print("true Hillary")
    elif str(testSet[randT][1]) == "realDonaldTrump":
        print("false Hillary")
elif max == cTru:
    if str(testSet[randT][1]) == "realDonaldTrump":
        print("true Trump")
    elif str(testSet[randT][1]) == "HillaryClinton":
        print("false Trump")
else:
    print("Something is seriously wrong!")
    print("Label was "+str(testSet[randT][1]))

db.close()
t1 = time.time()
print("Total time: "+str(t1-t0))