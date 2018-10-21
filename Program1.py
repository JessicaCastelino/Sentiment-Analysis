!pip install tweepy
!pip install elasticsearch
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch
import certifi
import time

# create instance of elasticsearch
es = Elasticsearch(
    [
    'https://portal-ssl1979-0.bmix-dal-yp-bba77080-b433-4072-bc85-9d26e6b2dbeb.2723981415.composedb.com:58058'],
    http_auth=('admin', 'WBJHGVXUZOZMHUVZ'),
      port=20202,
      use_ssl=True,
      verify_certs=True,
      ca_certs=certifi.where(),
)

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

consumer_key = "M6O2HMC2QBgB0M3ISmmvNBT0v"
consumer_secret = "LBfOuZmnDwcWQYWQEz1tz89rgyIHEaQkkzORFkNwhK2660qG62"
access_key = "1044944032215060480-fwOHg4cEm5dplmenkfS5d9rS3Y8BPK"
access_secret = "VhAchiXF9mGKmxlKESKYds9yQTyxOQzBYdFs9g8IEUdIh"

class TweetStreamListener(StreamListener):
    
    def __init__(self, time_limit=500):
        self.start_time = time.time()
        self.limit = time_limit
        super(TweetStreamListener, self).__init__()
        
    # on success   
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            dict_data = json.loads(data)
            print(dict_data['text'])
            es.index(index="mlib3",doc_type="sentimentanalysismlib",body={"id": dict_data["id_str"],
                        "author": dict_data["user"]["screen_name"], 
                        "date": dict_data["created_at"],
                        "text": clean_tweet(dict_data["text"])})
            return True
        else:
            return False        
        

    # on failure
    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()
    
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(track=['food'])