import tweepy
from msr import MyStreamListener

consumer_key = "******************************"
consumer_secret = "*************************"
access_token = "*********************"
access_token_secret = "**********************"

au = tweepy.OAuthHandler(consumer_key, consumer_secret)
au.set_access_token(access_token, access_token_secret)
api = tweepy.API(au)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['trump'])
