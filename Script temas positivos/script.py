import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch

# import twitter keys and tokens
ckey = "Lz3BzqoqPJA7hrLE7XnYOncdH"
csecret = "1MRn8ElY8Ea24HBSXCvIrVTR0rx3vWA8WFOgEtaTH8SfBQ4uY1"
atoken = "742503304056459264-a8gYllNQEpKAP3O8f73cUgUcoyIdZ0D"
asecret = "LO4oZ55UiXWBlFPuvub78TcDt1vTjAzNYaOecOMMXoK6q"

# create instance of elasticsearch
es = Elasticsearch()


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)

        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])

        # output sentiment polarity
        print (tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        print (sentiment)

        # add text and sentiment info to elasticsearch
        es.index(index="data2",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "geo":dict_data["user"]["location"],
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment})
        return True

    # on failure
    def on_error(self, status):
        print (status)

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)


    stream.filter(locations=[-168.0,-56.1,-33.7,70.8])


    
