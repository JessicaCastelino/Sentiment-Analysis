import pandas as pd
import pyspark as ps
import csv
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import Tokenizer
from pyspark.sql.functions import col, udf 
from pyspark.sql.types import IntegerType
import re
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.types import StringType
from elasticsearch import Elasticsearch
import certifi
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

#Removes emojis and punctuations from the tweet
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#Creating SparkContext and SQLContext
sc.stop()
sc = SparkContext("local[2]")
sqlContext = SQLContext(sc)

#Testing data fetched from elasticsearch
es = Elasticsearch(
    [
    'https://portal-ssl1979-0.bmix-dal-yp-bba77080-b433-4072-bc85-9d26e6b2dbeb.2723981415.composedb.com:58058'],
    http_auth=('admin', 'WBJHGVXUZOZMHUVZ'),
      port=20202,
      use_ssl=True,
      verify_certs=True,
      ca_certs=certifi.where(),
)
res = es.search(index="mlib3", doc_type="sentimentanalysismlib", body={"_source": ["id","text"], "query": {"match_all": {}}}, size=2000)
testing_df=pd.DataFrame.from_dict(res['hits']['hits'])
testing_df=testing_df.drop(columns=['_id','_index','_score','_type'])
testing_df=pd.concat(map(pd.DataFrame.from_dict, res['hits']['hits']), axis=1)['_source'].T
testing_df=testing_df.reset_index(drop=True)
testing_df.to_csv("tweets.csv",sep=',',encoding='utf-8')
#testingData.printSchema()


#Training data Tweets_training.csv is converted to TrainingData.csv
#The values for sentiments are converted from labels to numbers - 0 implies neutral, 1 implies positive and 2 implies negative
filename=r"Tweets_training.csv"
outputFile=r"TrainingData.csv"
tweetsFile = open(filename, "rt", encoding="utf-8")
reader = csv.reader(tweetsFile)
newRows = []
for row in reader:
    if(row[1]=='neutral'):
        sentiment=0
    elif(row[1]=='positive'):
        sentiment=1
    elif(row[1]=='negative'):
        sentiment=2
    else:
        sentiment='label'
    newRow = [clean_tweet(row[10]).encode("ascii","ignore").decode("utf-8"), sentiment]
    newRows.append(newRow)
tweetsFile.close()

# Do the writing
trainingFile = open(outputFile, 'wt', encoding="utf-8",newline='')
writer = csv.writer(trainingFile)
writer.writerows(newRows)
trainingFile.close()

trainingFile = open(outputFile,"r")
pandas_df = pd.read_csv(trainingFile)
spark_df = sqlContext.createDataFrame(pandas_df)

#Pipeline
countTokens = udf(lambda words: len(words), IntegerType())
tokenizer = Tokenizer(inputCol="text", outputCol="new_text")
add_stopwords = ["http","https","amp","RT","the"] 
stopwordsRemover = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="filtered").setStopWords(add_stopwords)
cv = CountVectorizer(inputCol=stopwordsRemover.getOutputCol(), outputCol="features", vocabSize=3, minDF=2.0)
lr= LogisticRegression(maxIter=20, regParam=0.001)
pipeline = Pipeline(stages=[tokenizer, stopwordsRemover, cv, lr])
model = pipeline.fit(spark_df)

#Sentiments Predicted
testingData=sqlContext.createDataFrame(testing_df)
prediction = model.transform(testingData)
selected = prediction.select("text", "probability", "prediction")
for row in selected.collect():
    text, prob, prediction = row
    print("(%s) --> prob=%s, prediction=%d" % (text, str(prob), prediction))
	
#Evaluating the model's accuracy
(train, test) = spark_df.randomSplit([0.7, 0.3], seed = 100)
print("Training data count: "+str(train.count()))
print("Testing data count: "+str(test.count()))
newModel=pipeline.fit(train)
predictions = newModel.transform(test)
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
accuracy = evaluator.evaluate(predictions)
print("Accuracy of model: "+str(accuracy))