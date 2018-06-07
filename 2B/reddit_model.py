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
  join = labeled_data.join(comments, labeled_data['Input_id'] == comments['id'], 'inner')

  #TASK 4,5
  sanitizeWithPython = udf(sanitize, ArrayType(StringType()))
  splitGramsWithPython = udf(split_grams, ArrayType(StringType()))
  #grams_df = join.select("id", sanitizeWithPython("body").alias("grams"))
  grams_df = join.select("id", "labeldjt", splitGramsWithPython(sanitizeWithPython("body")).alias("grams"))
  #print(grams_df.dtypes)

  #TASK 6A
  cv = CountVectorizer(inputCol="grams", outputCol="features", minDF=5)
  cv_df = cv.fit(grams_df)
  result = cv_df.transform(grams_df)
  #result.show(truncate=False)

  #TASK 6B
  changePosWithPython = udf(change_pos, IntegerType())
  grams_df = grams_df.withColumn("posSent",changePosWithPython("labeldjt"))
  grams_df.show(n=10)

if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
