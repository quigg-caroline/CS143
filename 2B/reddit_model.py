#!/usr/local/bin/python

from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

# IMPORT OTHER MODULES HERE
import os
from pyspark.sql.functions import udf
from cleantext import sanitize
from pyspark.ml.feature import CountVectorizer
from pyspark.sql.types import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, CrossValidatorModel
from pyspark.ml.evaluation import BinaryClassificationEvaluator

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
  '''
  # Once we train the models, we don't want to do it again. We can save the models and load them again later.
  #posModel.save("www/pos.model")
  #negModel.save("www/neg.model")
  

  #TASK 8
  stripIdWithPython = udf(strip_id, StringType())
  comments = commentpar.select('id', 'body', stripIdWithPython('link_id').alias('link_id'), 'created_utc', 'author_flair_text')
  submissions = submissionspar.select('id','title')
  submissions = submissions.withColumnRenamed('id', 'submission_id')
  comment_data_df = comments.join(submissions, comments['link_id'] == submissions['submission_id'], 'inner')
  #comment_data_df.show(n=10)

  #TASK 9
  unlabeled_df = comment_data_df.select("id", "body", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"), "title", "created_utc", "author_flair_text")
  #unlabeled_df.show(n=10)
  unlabeled_result = cv_df.transform(unlabeled_df)
  #unlabeled_result.show(n=10)
  unlabeled_result.createGlobalTempView("unlabeled_view")
  unlabeled_result = context.sql("SELECT * FROM global_temp.unlabeled_view WHERE body NOT LIKE '%/s%' AND body NOT LIKE '&gt%' ")
  posModel = CrossValidatorModel.load("pos.model")
  negModel = CrossValidatorModel.load("neg.model")
  posResult = posModel.transform(unlabeled_result)
  posResult = posResult.withColumnRenamed('probability','pos_prob')
  posResult = posResult.withColumnRenamed('rawPrediction','pos_raw')
  posResult = posResult.withColumnRenamed('prediction','pos_pred')
  result = negModel.transform(posResult)
  #posResult.show(n=10)
  #negResult.show(n=10)
  labelPosWithPython = udf(label_pos, IntegerType())
  labelNegWithPython = udf(label_neg, IntegerType())
  sentiment = result.withColumn("pos", labelPosWithPython("pos_prob"))
  sentiment = sentiment.withColumn("neg", labelNegWithPython("probability")).select("id","body","title","created_utc","author_flair_text","pos","neg")
  sentiment.show(n=5)



if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
