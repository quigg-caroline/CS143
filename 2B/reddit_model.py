#!/usr/local/bin/python

from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, functions as F

# IMPORT OTHER MODULES HERE
import os
import time
from pyspark.sql.functions import udf
from cleantext import sanitize
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.types import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, CrossValidatorModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from states import US_STATES

############## MACHINE LEARNING STUFF ###########################

def getClassifierModels(posResult, negResult):
    posModel = None
    negModel = None
    if (os.path.isdir('www/pos.model') and os.path.isdir('www/neg.model')):
        posModel = CrossValidatorModel.load("www/pos.model")
        negModel = CrossValidatorModel.load("www/neg.model")
        print("Using saved models")
    else:
        print("Building models")
        posModel, negModel = buildModels(posResult, negResult)
        posModel.save("www/pos.model")
        negModel.save("www/neg.model")
    
    return posModel, negModel

def buildModels(posResult, negResult):
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
    return posModel, negModel
    
#######################################################################

def writeToFile(dataframe, filename):
  dataframe.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save(filename)

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
  
def printTaskFinishMessage(i):
  print(f"{time.asctime()}: Finished task {i}")


def buildSentimentsDF(context):
  ##### TASK 1: Load data into PySpark
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
  printTaskFinishMessage('1')

  ##### TASK 2
  comments = commentpar.select('id', 'body')
  comment_df = labeled_data.join(comments, labeled_data['Input_id'] == comments['id'], 'inner')
  printTaskFinishMessage('2')

  ##### TASK 4,5
  sanitizeWithPython = udf(sanitize, ArrayType(StringType()))
  splitGramsWithPython = udf(split_grams, ArrayType(StringType()))
  #grams_df = join.select("id", sanitizeWithPython("body").alias("grams"))
  grams_df = comment_df.select("id", "labeldjt", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"))
  printTaskFinishMessage('4/5')

  ##### TASK 6A - 
  cv = CountVectorizer(inputCol="grams", outputCol="features", minDF=5)
  cv_df = cv.fit(grams_df)
  result = cv_df.transform(grams_df)
  printTaskFinishMessage('6A')

  ##### TASK 6B
  changePosWithPython = udf(change_pos, IntegerType())
  posResult = result.withColumn("label",changePosWithPython("labeldjt"))
  #grams_df.show(n=10)
  changeNegWithPython = udf(change_neg, IntegerType())
  negResult = result.withColumn("label",changeNegWithPython("labeldjt"))

  ################################
  ##### TASK 7 - Train model #####
  ################################

  # 7A Get classifier models, building them if they don't exist as saved files already
  posModel, negModel = getClassifierModels(posResult, negResult)
  printTaskFinishMessage('7')

  #######################################################
  ##### TASK 8 - Read in the full comments data now #####
  #######################################################

  stripIdWithPython = udf(strip_id, StringType())

  # 8A Grab the title and score of the original post
  context.registerDataFrameAsTable(submissionspar, 'submissions')
  submissions = context.sql('''
    SELECT id as submission_id, title, score as submission_score
    FROM submissions
  ''')

  # 8B Grab all the data we need from the comment
  context.registerDataFrameAsTable(commentpar, 'comments')
  context.registerFunction('stripIdt3', lambda s: s[3:])
  comments = context.sql('''
    SELECT id as comment_id, body, stripIdt3(link_id) as link_id, created_utc, author_flair_text, score as comment_score
    FROM comments
  ''')

  # 8C Join the original post with the comment data so we know which post each comment was for
  # Add a column with the comment's grams as well
  commentsAndPosts = comments\
    .join(submissions, comments['link_id'] == submissions['submission_id'], 'inner')\
    .withColumn('grams', splitGramsWithPython(sanitizeWithPython("body")))

  printTaskFinishMessage('8')

  ################################################
  ##### TASK 9 - Build full sentiments table #####
  ################################################

  # 9A Select out comment id, comment content, grams, submission title, timestamp, and state info in author_flair_text
  # unlabeled_df = commentsAndPosts.select("comment_id","link_id", "body", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"), "title", "created_utc", "author_flair_text")
  # comments
  # printTaskFinishMessage('9A')
  
  # 9B Transform using the unlabeled data (??? what does this MEAN???), filter out sarcasm and quoted submissions
  unlabeled_result = cv_df\
    .transform(commentsAndPosts)\
    .where("body NOT LIKE '%/s%' AND body NOT LIKE '&gt%'")
  printTaskFinishMessage('9B')

  # 9C Transform for positive model
  posResult = posModel.transform(unlabeled_result)\
    .withColumnRenamed('probability','pos_prob')\
    .withColumnRenamed('rawPrediction','pos_raw')\
    .withColumnRenamed('prediction','pos_pred')
  printTaskFinishMessage('9C')

  # 9D Transform for negative model
  result = negModel.transform(posResult)\
    .withColumnRenamed('probability','neg_prob')\
    .withColumnRenamed('rawPrediction','neg_raw')\
    .withColumnRenamed('prediction','neg_pred')
  printTaskFinishMessage('9D')

  labelPosWithPython = udf(label_pos, IntegerType())
  labelNegWithPython = udf(label_neg, IntegerType())

  fraction = 0.2
  # 9E Use the probabilities for positive and negative values to label 1/0 for each comment's pos/neg
  sentiments = result\
    .withColumn("pos", labelPosWithPython("pos_prob"))\
    .withColumn("neg", labelNegWithPython("neg_prob"))\
    .select("comment_id", "link_id", "title", "created_utc", "author_flair_text", "pos", "neg", "submission_score", "comment_score")\
    .sample(False, fraction, None)
  
  printTaskFinishMessage('9E')
  return sentiments

def main(context):
  """Main function takes a Spark SQL context."""
  # YOUR CODE HERE
  # YOU MAY ADD OTHER FUNCTIONS AS NEEDED
  
  sentiments = None
  if (os.path.isdir('sentiments.parquet')):
    sentiments = context.read.parquet('sentiments.parquet')
  else:
    sentiments = buildSentimentsDF(context)
    sentiments.show()
    sentiments.write.parquet('sentiments.parquet')

  #################################################
  ##### TASK 10 - Compute various percentages #####
  #################################################

  # Set up temporary sentiments SQL table for querying
  context.registerDataFrameAsTable(sentiments, 'sentiments_table')
  aggregator = 'SUM(pos) / COUNT(*) AS percent_positive, SUM(neg) / COUNT(*) AS percent_negative'

  # 10A Aggregate comments within a submission, calculating percentage
  # Using MAX(submission_score) but they should all be the same since it's
  # grouped by link_id
  submissionCSVName = 'submissions.csv.data'
  if (not os.path.isdir(submissionCSVName)):
    submission_aggregate = context.sql(f'''
      SELECT link_id, MAX(submission_score) AS submission_score, {aggregator}
      FROM sentiments_table
      GROUP BY link_id
    ''')
    writeToFile(submission_aggregate, submissionCSVName)
  printTaskFinishMessage('10A')

  # 10B Aggregate comments within each day
  timeDataCSVName = 'time_data.csv.data'
  if (not os.path.isdir(timeDataCSVName)):
    cross_day_aggregate = context.sql(f'''
      SELECT t.date, SUM(t.pos) / COUNT(*) AS percent_positive, SUM(t.neg) / COUNT(*) AS percent_negative
      FROM (
        SELECT DATE(FROM_UNIXTIME(created_utc)) AS date, pos, neg
        FROM sentiments_table
      ) t
      GROUP BY date
    ''')
    writeToFile(cross_day_aggregate, timeDataCSVName)
  printTaskFinishMessage('10B')

  # 10C Aggregate comments across states
  stateDataCSVName = 'state_data.csv.data'
  if (not os.path.isdir(stateDataCSVName)):
    cross_state_aggregate = context.sql(f'''
      SELECT author_flair_text AS state, {aggregator} 
      FROM sentiments_table
      WHERE author_flair_text IN ({", ".join(map(lambda s: f"'{s}'", US_STATES))})
      GROUP BY author_flair_text
    ''')
    writeToFile(cross_state_aggregate, stateDataCSVName)
  printTaskFinishMessage('10C')

  # 10D By comment score
  commentScoresCSVName = 'comment_scores.csv.data'
  if (not os.path.isdir(commentScoresCSVName)):
    top_10_comment_scores = context.sql(f'''
      SELECT comment_score, {aggregator}
      FROM sentiments_table
      GROUP BY comment_score
      ORDER BY comment_score DESC
    ''')
    # 10D.1 Show top 10 comments by score
    writeToFile(top_10_comment_scores, commentScoresCSVName)
  printTaskFinishMessage('10D')

  # 10E By submission score
  submissionScoresCSVName = 'submission_scores.csv.data'
  submission_scores = None
  if (not os.path.isdir(submissionScoresCSVName)):
    submission_scores = context.sql(f'''
      SELECT MIN(title) AS title, submission_score, {aggregator}
      FROM sentiments_table
      GROUP BY submission_score
      ORDER BY submission_score DESC
    ''')
    writeToFile(submission_scores, submissionScoresCSVName)
  
    # Save the top 10 submissions list too if it hasn't been done yet
    top10SubsCSVName = 'top_10_submissions.csv.data'
    top10 = submission_scores.orderBy("submission_score", ascending=False).limit(10)
    writeToFile(top10, top10SubsCSVName)

  printTaskFinishMessage('10')


  # 10F Get top 10 lists


  return

if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
