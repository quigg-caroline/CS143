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
  result = result.select('grams', 'labeldjt', 'features')

  #TASK 6B
  changePosWithPython = udf(change_pos, IntegerType())
  posResult = result.withColumn("label",changePosWithPython("labeldjt"))
  posResult = posResult.select('grams', 'label', 'features')

  #grams_df.show(n=10)
  changeNegWithPython = udf(change_neg, IntegerType())
  negResult = result.withColumn("label",changeNegWithPython("labeldjt"))
  negResult = negResult.select('grams', 'label', 'features')
  '''
  #TASK 7
  # Initialize two logistic regression models.
  # Replace labelCol with the column containing the label, and featuresCol with the column containing the features.
  poslr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
  neglr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
  # This is a binary classifier so we need an evaluator that knows how to deal with binary classifiers.
  posEvaluator = BinaryClassificationEvaluator()
  negEvaluator = BinaryClassificationEvaluator()
  # There are a few parameters associated with logistic regression. We do not know what they are a priori.
  # We do a grid search to find the best parameters. We can replace [1.0] with a list of values to try.
  # We will assume the parameter is 1.0. Grid search takes forever.
  posParamGrid = ParamGridBuilder().addGrid(poslr.regParam, [1.0]).build()
  negParamGrid = ParamGridBuilder().addGrid(neglr.regParam, [1.0]).build()
  # We initialize a 5 fold cross-validation pipeline.
  posCrossval = CrossValidator(
      estimator=poslr,
      evaluator=posEvaluator,
      estimatorParamMaps=posParamGrid,
      numFolds=5)
  negCrossval = CrossValidator(
      estimator=neglr,
      evaluator=negEvaluator,
      estimatorParamMaps=negParamGrid,
      numFolds=5)
  # Although crossvalidation creates its own train/test sets for
  # tuning, we still need a labeled test set, because it is not
  # accessible from the crossvalidator (argh!)
  # Split the data 50/50
  posTrain, posTest = posResult.randomSplit([0.5, 0.5])
  negTrain, negTest = negResult.randomSplit([0.5, 0.5])
  # Train the models
  print("Training positive classifier...")
  posModel = posCrossval.fit(posTrain)
  print("Training negative classifier...")
  negModel = negCrossval.fit(negTrain)
  posModel.save("www/pos.model")
  negModel.save("www/neg.model")
  '''
  #TASK 8
  stripIdWithPython = udf(strip_id, StringType())

  # Build submissions
  submissions = submissionspar\
    .select('id','title', 'score')\
    .withColumnRenamed('id', 'submission_id')\
    .withColumnRenamed('score', 'sub_score')

  # Build comment data
  comments = commentpar.select('id', 'body', 'score', stripIdWithPython('link_id').alias('link_id'), 'created_utc', 'author_flair_text')\
    .withColumnRenamed('score', 'comments_score')
  comment_data_df = comments.join(submissions, comments['link_id'] == submissions['submission_id'], 'inner')

  #TASK 9
  # Select out comment id, comment content, grams, submission title, timestamp, and state info in author_flair_text
  unlabeled_df = comment_data_df.select("id", "link_id", 'comments_score', 'sub_score', splitGramsWithPython(sanitizeWithPython("body")).alias("grams"), "created_utc", 'title', "author_flair_text")\
    .withColumnRenamed('author_flair_text', 'state')\
    .withColumnRenamed('created_utc', 'timestamp')
  # Transform using the unlabeled data (??? what does this MEAN???)
  # Filter out sarcasm and quoted submissions
  unlabeled_result = cv_df\
    .transform(unlabeled_df)\
    .where("body NOT LIKE '%/s%' AND body NOT LIKE '&gt%'")

  # Load our trained models
  posModel = CrossValidatorModel.load("www/pos.model")
  negModel = CrossValidatorModel.load("www/neg.model")

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
    .select("id","link_id", "title","timestamp","state","pos","neg")
    #.sample(False, 3/3000000)
  sentiments = sentiments.sample(False, 0.2, None)

  print("task 9 to parquet")
  sentiments.write.parquet("sentiments.parquet")
  sentiment_p = context.read.parquet("comments.parquet")
  #print("HERE")
  #bleh.write.csv("lol_fucking_l")
  #sentiments.repartition(1).write.format("com.databricks.spark.csv").save("finalResult.csv")

  print("Task 10")
  #TASK 10 - Compute percentages of shit
  '''
  sentiments = sentiments.groupBy('link_id') \
    .agg(F.sum('pos'), F.sum('neg'))\
    .select('sub_score', 'pos', 'neg')
  '''
  sentiment_p.registerTempTable('sentiment_result')
  state_query = 'SELECT state, Sum(pos)/Count(state) AS Positive, Sum(neg)/Count(state) AS Negative FROM sentiment_result GROUP BY state'
  time_query = 'SELECT FROM_UNIXTIME(Timestamp, \'%Y-%d-%M\') as date, SUM(pos)/Count(FROM_UNIXTIME(Timestamp, \'%Y-%d-%M\')) as Positive, SUM(neg)/COUNT(FROM_UNIXTIME(Timestamp, \'%Y-%d-%M\')) as Negative FROM sentiment_result GROUP BY FROM_UNIXTIME(Timestamp, \'%Y-%d-%M\')'
  str_query_sub = 'SELECT sub_id, Sum(pos)/Count(sub_id) AS Positive, Sum(neg)/Count(sub_id) AS Negative FROM sentiment_result GROUP BY sub_id'
  str_query_subs = 'SELECT submissions_score AS submission_core, Sum(pos)/Count(submissions_score) AS Positive, Sum(neg)/Count(submissions_score) AS Negative FROM sentiment_result GROUP BY submissions_score'
  str_query_comments = 'SELECT comments_score AS comment_score, SUM(pos)/Count(comments_score) as Positive, Sum(neg)/Count(comments_score) as Negative FROM sentiment_result GROUP BY comments_score' 
  
  Print("run queries")
  df_sub = sqlContext.sql(str_query_sub)
  df_time = sqlContext.sql(time_query)
  df_states = sqlContext.sql(state_query)
  df_subs = sqlContext.sql(str_query_subs)
  df_comments = sqlContext.sql(str_query_comments)
  
  print('Writing')
  df_subs.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("submission_score.csv")
  df_comments.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("comment_score.csv")
  df_sub.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("other_submissions.csv") 
  df_time.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("time_data.csv")  
  df_states.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("state_data.csv")

  # Load parquet file into a data frame variable
  # submission_aggregate = context.sql('''
  #   SELECT title, SUM(pos) as percent_positive, SUM(neg) as percent_negative
  #   FROM global_temp.sentiments_view
  #   GROUP BY title
  # ''').show(n=10)


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
