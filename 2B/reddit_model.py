#!/usr/local/bin/python

from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

# IMPORT OTHER MODULES HERE
import os

#TASK 1: Load data into PySpark
#Written as a parquet file so should only take 10+ minutes to run the first time
def load(context):
  
  if os.path.isdir('comments.parquet') == False:
    comments = context.read.json("comments-minimal.json.bz2")
    comments.write.parquet("comments.parquet")
  commentpar = context.read.parquet("comments.parquet")

  if os.path.isdir('submissions.parquet') == False:
    submissions = context.read.json("submissions.json.bz2")
    submissions.write.parquet("submissions.parquet")
  submissionspar = context.read.parquet("submissions.parquet")

  if os.path.isdir('labeled_data.parquet') == False:
    labeled_data = context.read.csv("labeled_data.csv")
    labeled_data.write.parquet("labeled_data.parquet")
  datapar = context.read.parquet("labeled_data.parquet")

def main(context):
  """Main function takes a Spark SQL context."""
  # YOUR CODE HERE
  # YOU MAY ADD OTHER FUNCTIONS AS NEEDED
  
  #Task 1
  load(context)

if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
