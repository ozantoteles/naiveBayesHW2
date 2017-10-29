import tweepy
import json

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        with open("dump\\"+str(status.id)+'.json', 'w') as fp:
            json.dump(status._json, fp)

    def on_error(self, status_code):
        if status_code == 420:
            return False