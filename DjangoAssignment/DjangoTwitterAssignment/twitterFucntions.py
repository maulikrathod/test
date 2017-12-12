#  Import Tweepy module
import tweepy

# Auth Keys
consumer_key = "EeK3BcGakBKTyhak7CDxJOZiA"
consumer_secret = "8wUJfeZBrOv3M6QskaUiYnkFzTwFS103KHKrqohtH3N4NUE8lC"
access_token = "939658649806389248-fU28bCP3dw8nErR0JFZSuSbUHSctjiw"
access_token_secret = "XBjEn7DWq8REBHoYuiubGchz8fdbZL3A1Tw2BBzWmSaYU"

# creating authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# setting your access tocken and secret
auth.set_access_token(access_token, access_token_secret)

# Creating api object while passing auth information
api = tweepy.API(auth)

# Get tweets from handle
def get_tweet_from_name(name):
    tweetCount = 10
    results = api.user_timeline(id=name, count=tweetCount)
    top_tweets = []
    for tweet in results:
        # if (not tweet.retweeted) and ('RT @' not in tweet.text):
        top_tweets.append(tweet.text)
    return top_tweets

#  FIND TOTAL NO OF FOLLOWERS
def find_followers(name):
    try:
        user = api.get_user(name)
        return user.followers_count
    except tweepy.TweepError as e:
        return (e.reason)

# find following count
def following(name):
    try:
        user = api.get_user(name)
        return user.friends_count
    except tweepy.TweepError as e:
        return (e.reason)

# Get tweets based on datewise
def get_tweets(name, tweetCount):
    Count = tweetCount
    results = api.user_timeline(id=name, count=tweetCount)
    tweets_list = []
    for tweet in results:
        tweets_dict = {}
        tweets_dict['name'] = name
        tweets_dict['date'] = tweet.created_at
        tweets_dict['tweets'] = tweet.text
        tweets_list.append(tweets_dict)
    return(tweets_list)
