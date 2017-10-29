import tweepy
from msr import MyStreamListener

consumer_key = "1jZs5hCfFKovOaQT15z5zQsbe"
consumer_secret = "yZiiIo0J3i8n2qVweDMcOcnN9q9mIZcdgnDs0bGGWTPOWiJ1Ib"
access_token = "275816839-Ps7bIJ2lKJdYMxgHOojB1CcsPZvIXkxGjpAH5l6V"
access_token_secret = "9Ei4yIudGqP6fhK6O5CQF2tc4lSLyG3fxwgRELHESzGU7"

au = tweepy.OAuthHandler(consumer_key, consumer_secret)
au.set_access_token(access_token, access_token_secret)

api = tweepy.API(au)


# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#    print(tweet.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['trump'])
