#!/usr/local/bin/python

from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

# IMPORT OTHER MODULES HERE
import os

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

  #labeled_data = context.read.csv("labeled_data.csv")
  labeled_data = context.read.load("labeled_data.csv", format="csv", sep=",", inferSchema="true", header="true")

  #TASK 2
  #labeled_data.join(commentpar.select("id"), "Input_id").show()
  #context.sql("SELECT * FROM labeled_data l JOIN commentpar c ON l.Input_id = c.id").show()
  comments = commentpar.select('id', 'body')
  join = labeled_data.join(comments, labeled_data['Input_id'] == comments['id'], 'inner')

if __name__ == "__main__":
  conf = SparkConf().setAppName("CS143 Project 2B")
  conf = conf.setMaster("local[*]")
  sc   = SparkContext(conf=conf)
  sqlContext = SQLContext(sc)
  sc.addPyFile("cleantext.py")

  main(sqlContext)
