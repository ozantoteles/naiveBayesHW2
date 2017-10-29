import json
import os
from pprint import pprint
import sqlite3


db = sqlite3.connect('data/trumpdb')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY, tid INT, tweet TEXT, tweetNP TEXT, tweetNPSW TEXT, class TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY, word TEXT, count INTEGER NOT NULL DEFAULT 0, likeCount INTEGER NOT NULL DEFAULT 0, dislikeCount INTEGER NOT NULL DEFAULT 0, neutralCount INTEGER NOT NULL DEFAULT 0, irrelevantCount INTEGER NOT NULL DEFAULT 0, UNIQUE(word))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS wordsp(id INTEGER PRIMARY KEY, word TEXT, plike FLOAT, pdislike FLOAT, pneutral FLOAT, pirrelevant FLOAT, UNIQUE(word))''')
db.commit()

punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’…'
stopWordsNoP = ["rt","a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"]

def stopWordRemover (text, swords):
    return list(set([word for word in text.split() if word.lower() not in swords]))

def linkRemover (text):
    #return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('@') or word.lower().startswith('http'))]))
    return list(set([word for word in text.split() if not (word.lower().startswith('www.') or word.lower().startswith('http'))]))

for jsonFilename in os.listdir('dumpLimited'):
    with open("dumpLimited\\"+jsonFilename) as json_file:
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


        #pprint(tweetNP)
        pprint(tweetNPSW)
        print("-------------\n\n")
        #pprint(classOf)

        cursor.execute('''INSERT INTO tweets(tid, tweet, tweetNP, tweetNPSW, class) VALUES(?,?,?,?,?)''', (tid, tweet, tweetNP, tweetNPSW, classOf))

        words = tweetNPSW.split()

        for word in words:
            cursor.execute('''INSERT OR IGNORE INTO words(word) VALUES(?)''', (word,))
            cursor.execute('''UPDATE words SET count = count + ? WHERE word = ?''', (1, word))
            if label == "l":
                cursor.execute('''UPDATE words SET likeCount = likeCount + ? WHERE word = ?''', (1, word))
            elif label == "d":
                #classOf = "disliked"
                cursor.execute('''UPDATE words SET dislikeCount = dislikeCount + ? WHERE word = ?''', (1, word))
            elif label == "n":
                #classOf = "neutral"
                cursor.execute('''UPDATE words SET neutralCount = neutralCount + ? WHERE word = ?''', (1, word))
            elif label == "i":
                #classOf = "irrelevant"
                cursor.execute('''UPDATE words SET irrelevantCount = irrelevantCount + ? WHERE word = ?''', (1, word))
            else:
                #classOf = "irrelevant"
                cursor.execute('''UPDATE words SET irrelevantCount = irrelevantCount + ? WHERE word = ?''', (1, word))


        #label = input("Press l for like, d for dislike, n for neutral, i for irrelevant \n")

        db.commit()

cursor.execute('''SELECT class from tweets''')
tweets = cursor.fetchall()
tweetCount = float(len(tweets))
tLikeCount = float(tweets.count(('liked',)))/tweetCount # p(liked)
tDislikeCount = float(tweets.count(('disliked',)))/tweetCount # p(disliked))
tNeutralCount = float(tweets.count(('neutral',)))/tweetCount # p(neutral))
tIrrelevantCount = float(tweets.count(('irrelevant',)))/tweetCount # p(irrelevant))
print('There are '+str(tweetCount)+' tweets in the database\n'+str(tLikeCount)+' labeled as Liked\n'+str(tDislikeCount)+' labeled as Disliked\n'+str(tNeutralCount)+' labeled as Neutral\n'+str(tIrrelevantCount)+' labeled as Irrelevant\n')

cursor.execute('''SELECT word FROM words''')
wordCount = float(len(cursor.fetchall()))
print('There are '+str(wordCount)+' words in the database')

cursor.execute('''SELECT likeCount from words''')
likeCount = cursor.fetchall()
likeCount = float(len(likeCount) - likeCount.count((0,)))
print('There are '+str(likeCount)+' liked labeled words in the database')

cursor.execute('''SELECT dislikeCount from words''')
dislikeCount = cursor.fetchall()
dislikeCount = float(len(dislikeCount) - dislikeCount.count((0,)))
print('There are '+str(dislikeCount)+' disliked labeled words in the database')

cursor.execute('''SELECT irrelevantCount from words''')
irrelevantCount = cursor.fetchall()
irrelevantCount = float(len(irrelevantCount) - irrelevantCount.count((0,)))
print('There are '+str(irrelevantCount)+' irrelevant labeled words in the database')

cursor.execute('''SELECT neutralCount from words''')
neutralCount = cursor.fetchall()
neutralCount = float(len(neutralCount) - neutralCount.count((0,)))
print('There are '+str(neutralCount)+' neutral labeled words in the database')

cursor.execute('''SELECT sum(likeCount) FROM words''')
likedWordOccurances = float(cursor.fetchall()[0][0])

cursor.execute('''SELECT sum(dislikeCount) FROM words''')
dislikedWordOccurances = float(cursor.fetchall()[0][0])

cursor.execute('''SELECT sum(neutralCount) FROM words''')
neutralWordOccurances = float(cursor.fetchall()[0][0])

cursor.execute('''SELECT sum(irrelevantCount) FROM words''')
irrelevantWordOccurances = float(cursor.fetchall()[0][0])

print(str(likedWordOccurances)+' words in liked tweets\n'+str(dislikedWordOccurances)+' words in disliked tweets\n'+str(neutralWordOccurances)+' words in neutral tweets\n'+str(irrelevantWordOccurances)+' words in irrelevant tweets\n')

cursor.execute('''SELECT * from words''')
rows = cursor.fetchall()
for row in rows:
    cursor.execute('''INSERT OR IGNORE INTO wordsp(word) VALUES(?)''', (row[1],))
    plike = (float(row[3])+1.0)/(likedWordOccurances+wordCount)*tLikeCount
    pdislike = (float(row[4])+1.0)/(likedWordOccurances+wordCount)*tDislikeCount
    pneutral = (float(row[5])+1.0)/(likedWordOccurances+wordCount)*tNeutralCount
    pirrelevant = (float(row[6])+1.0)/(likedWordOccurances+wordCount)*tIrrelevantCount
    cursor.execute('''UPDATE wordsp SET plike = ? WHERE word = ?''', (plike, row[1]))
    cursor.execute('''UPDATE wordsp SET pdislike = ? WHERE word = ?''', (pdislike, row[1]))
    cursor.execute('''UPDATE wordsp SET pneutral = ? WHERE word = ?''', (pneutral, row[1]))
    cursor.execute('''UPDATE wordsp SET pirrelevant = ? WHERE word = ?''', (pirrelevant, row[1]))
    db.commit()

db.close()