#!/usr/local/bin/python

from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F

# IMPORT OTHER MODULES HERE
import os
from pyspark.sql.functions import udf
from cleantext import sanitize
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.types import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, CrossValidatorModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from states import US_STATES

def split_grams(grams):
  grams = grams[1:]
  split = list()
  for i in grams:
    j = i.split()
    split = split + j
  return split

def change_pos(trump):
  #if poslabeld
  if trump == 1:
    return 1
  else:
    return 0

def change_neg(trump):
  #if poslabeld
  if trump == -1:
    return 1
  else:
    return 0

def label_pos(probability):
  if probability[1] > 0.2:
    return 1
  else:
    return 0

def label_neg(probability):
  if probability[1] > 0.25:
    return 1
  else:
    return 0

def strip_id(id):
  return id[3:]
  
def main(context):
  """Main function takes a Spark SQL context."""
  # YOUR CODE HERE
  # YOU MAY ADD OTHER FUNCTIONS AS NEEDED
  
  #TASK 1: Load data into PySpark
  #Written as a parquet file so should only take 10+ minutes to run the first time
  if os.path.isdir('comments.parquet') == False:
    comments = context.read.json("comments-minimal.json.bz2")
    comments.write.parquet("comments.parquet")
  commentpar = context.read.parquet("comments.parquet")

  if os.path.isdir('submissions.parquet') == False:
    submissions = context.read.json("submissions.json.bz2")
    submissions.write.parquet("submissions.parquet")
  submissionspar = context.read.parquet("submissions.parquet")

  labeled_data = context.read.load("labeled_data.csv", format="csv", sep=",", inferSchema="true", header="true")

  #TASK 2
  comments = commentpar.select('id', 'body')
  comment_df = labeled_data.join(comments, labeled_data['Input_id'] == comments['id'], 'inner')

  #TASK 4,5
  sanitizeWithPython = udf(sanitize, ArrayType(StringType()))
  splitGramsWithPython = udf(split_grams, ArrayType(StringType()))
  #grams_df = join.select("id", sanitizeWithPython("body").alias("grams"))
  grams_df = comment_df.select("id", "labeldjt", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"))
  #print(grams_df.dtypes)

  #TASK 6A
  cv = CountVectorizer(inputCol="grams", outputCol="features", minDF=5)
  cv_df = cv.fit(grams_df)
  result = cv_df.transform(grams_df)
  #result.show(n=10)

  #TASK 6B
  changePosWithPython = udf(change_pos, IntegerType())
  posResult = result.withColumn("label",changePosWithPython("labeldjt"))
  #grams_df.show(n=10)
  changeNegWithPython = udf(change_neg, IntegerType())
  negResult = result.withColumn("label",changeNegWithPython("labeldjt"))


  # TASK 7 - Train model
  # Use code from ml.py

  #TASK 8
  stripIdWithPython = udf(strip_id, StringType())

  # Build submissions
  submissions = submissionspar\
    .select('id','title')\
    .withColumnRenamed('id', 'submission_id')

  # Build comment data
  comments = commentpar.select('id', 'body', stripIdWithPython('link_id').alias('link_id'), 'created_utc', 'author_flair_text')
  comment_data_df = comments.join(submissions, comments['link_id'] == submissions['submission_id'], 'inner')

  #TASK 9
  # Select out comment id, comment content, grams, submission title, timestamp, and state info in author_flair_text
  unlabeled_df = comment_data_df.select("id", "body", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"), "title", "created_utc", "author_flair_text")
  
  # Transform using the unlabeled data (??? what does this MEAN???)
  # Filter out sarcasm and quoted submissions
  unlabeled_result = cv_df\
    .transform(unlabeled_df)\
    .where("body NOT LIKE '%/s%' AND body NOT LIKE '&gt%'")

  # Load our trained models
  posModel = CrossValidatorModel.load("pos.model")
  negModel = CrossValidatorModel.load("neg.model")

  # Transform positive model with SQL query results
  posResult = posModel.transform(unlabeled_result)\
    .withColumnRenamed('probability','pos_prob')\
    .withColumnRenamed('rawPrediction','pos_raw')\
    .withColumnRenamed('prediction','pos_pred')

  result = negModel.transform(posResult)
  labelPosWithPython = udf(label_pos, IntegerType())
  labelNegWithPython = udf(label_neg, IntegerType())

  # sentiments = result.withColumn("pos", labelPosWithPython("pos_prob"))
  # sentiments = sentiments.withColumn("neg", labelNegWithPython("probability")).select("id","body","title","created_utc","author_flair_text","pos","neg")

  sentiments = result.withColumn("pos", labelPosWithPython("pos_prob"))\
    .withColumn("neg", labelNegWithPython("probability"))\
    .select("id","body","title","created_utc","author_flair_text","pos","neg")\
    .sample(False, 3/3000000)
  #print("HERE")
  #sentiments.show()
  #bleh.write.csv("lol_fucking_l")
  #sentiments.repartition(1).write.format("com.databricks.spark.csv").save("finalResult.csv")

  #TASK 10 - Compute percentages of shit
  # sentiments.groupBy('title') \
  #   .agg(F.sum('pos'), F.sum('neg')) \
  #   .show()

  # Load parquet file into a data frame variable
  # submission_aggregate = context.sql('''
  #   SELECT title, SUM(pos) as percent_positive, SUM(neg) as percent_negative
  #   FROM global_temp.sentiments_view
  #   GROUP BY title
  # ''').show(n=10)

  return

  """ cross_day_aggregate = context.sql('''
    SELECT 
      title, 
      date, 
      SUM(pos) / COUNT(*) as percent_positive, 
      SUM(neg) / COUNT(*) as percent_negative
    FROM (
      SELECT title, DATE(FROM_UNIXTIME(created_utc)) as date, pos, neg
      FROM global_temp.sentiments_view
    )
    GROUP BY date
  ''').show(n=10) """

if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
