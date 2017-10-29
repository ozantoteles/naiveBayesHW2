import sqlite3

db = sqlite3.connect('data/trumpdb')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY, tid INT, tweet TEXT, tweetNP TEXT, tweetNPSW TEXT, class TEXT)''')
db.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS words(id INTEGER PRIMARY KEY, word TEXT, count INTEGER NOT NULL DEFAULT 0, likeCount INTEGER NOT NULL DEFAULT 0, dislikeCount INTEGER NOT NULL DEFAULT 0, neutralCount INTEGER NOT NULL DEFAULT 0, irrelevantCount INTEGER NOT NULL DEFAULT 0, UNIQUE(word))''')
db.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS wordsp(id INTEGER PRIMARY KEY, word TEXT, plike FLOAT, pdislike FLOAT, pneutral FLOAT, pirrelevant FLOAT, UNIQUE(word))''')
db.commit()

db.close()