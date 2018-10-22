# Sentiment Analysis

Sentiment analysis is used to analyse the emotional and evaluative content to distinguish them as positive, negative and neutral. Most review sites use sentiment analysis for business purposes. Sentiment analysis on tweets can enable to distinguish a wider variety of data. Also, tweets have different characteristics in the data like hashtags, message length, emoticons which can make shapes up the means of carrying sentiment analysis. Sentiment analysis, also known as opinion mining, uses natural language processing to identify and categorize the emotion or attitude for textual data. It can be done on a document, sentence or multimedia content. Sentiment Analysis can be done using different machine learning algorithms like Decision tree classification, Logistic Regression, Linear Regression, etc.

### Prerequisites

Kindly install the below modules before running the code.

```
!pip install tweepy
!pip install pyspark
!pip install pandas
!pip install certifi
!pip install elasticsearch
```

### Deployment

Kindly perform the below steps to perform sentiment analysis:

```
1) Download the code from Git.
2) Ensure all prerequsites are satisfied.
3) Execute Program1.py which downloads the tweets in real-time and uploads it to the Elasticsearch DB.
4) Execute Program2.py which fetches the test data from Elasticsearch DB and predicts the sentiments based on the model created.
```

## Information about the files used
* `Program1.py`: Contains the program to fetch tweets using Streaming Twitter API and upload it to Elasticsearch DB.
* `Program2.py`: Contains the program to perform classification using apache Spark on the Twitter Data uploaded on Elasticsearch.
* `Tweets_training.csv`: Contains the training data which has the tweets and the sentiments : positive, negative and neutral.
* `TrainingData.csv`: This file is derived from Tweets_training.csv. It contains the tweet and the sentiment value. Value 0 implies neutral sentiment, 1 implies positive sentiment and 2 implies negative sentiment.
* `tweets.csv`: Contains the tweets fetched from Elasticsearch (testing data).

## Authors

* **Jessica Castelino**  
* **Shivani Desai**


## References

[1] “Creating DataFrame from ElasticSearch Results,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/25186148/creating-dataframe-from-elasticsearch-results. [Accessed: 21-Oct-2018].

[2] “read and write on same csv file,” Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/3146571/read-and-write-on-same-csv-file. [Accessed: 21-Oct-2018].