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