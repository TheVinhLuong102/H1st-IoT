#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("adatao.decisionTree, adatao.randomForest, adatao.gradientBoostedTrees Regression")

cluster_ip <- "qa.adatao.com"
username <- "qa1"
password = "letmetest1@"

test_that("adatao.decisionTree, adatao.randomForest, adatao.gradientBoostedTrees Regression", {

adatao.connect(cluster_ip, username=username, password = password) # QA cluster

adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster



# ---- prepare data ----
#df<-adatao.loadTable("resources/YearPredictionMSD.txt",sep=",")
#df<-adatao.loadTable("resources/churnTrainH.csv",sep=",")
#df<-adatao.loadTable("resources/GiveCredit_cs-training.csv",sep=",")


adatao.sql("drop table GiveCredit")
adatao.sql("create external table GiveCredit(rowid int, SeriousDlqin2yrs int, RevolvingUtilizationOfUnsecuredLines double, age double, 
 NumberOfTime3059DaysPastDueNotWorse double, DebtRatio double,MonthlyIncome double,
 NumberOfOpenCreditLinesAndLoans double, NumberOfTimes90DaysLate double,
 NumberRealEstateLoansOrLines double, NumberOfTime6089DaysPastDueNotWorse double, 
 NumberOfDependents double)
 ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
 WITH serdeproperties ( 
 'separatorChar' = ',', 
 'quoteChar' = '\"' 
 )
 STORED AS TEXTFILE LOCATION '/GiveCredit/'");


# adatao.sql("create external table GiveCredit(rowid int, v1 int, v2 double, v3 double,  v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 double, v10 double)
# ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
# WITH serdeproperties ( 
# 'separatorChar' = ',', 
# 'quoteChar' = '\"' 
# )
# STORED AS TEXTFILE LOCATION '/GiveCredit/'");

ddf <- adatao.sql2ddf("select * from GiveCredit")
nrow(ddf)
colnames(ddf)

prepData = adatao.cv.rs(data=ddf, numSplits = 1, trainingFraction = 0.7)
testData <- prepData[[1]]$test
trainingData = prepData[[1]]$train

regression_model <- seriousdlqin2yrs ~ revolvingutilizationofunsecuredlines + age + numberoftime3059dayspastduenotworse + debtratio + monthlyincome + numberofopencreditlinesandloans + numberoftimes90dayslate + numberrealestateloansorlines  + numberoftime6089dayspastduenotworse + numberofdependents




# ---- test decision tree model ---
dtModel <- adatao.decisionTree(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, minInstancePerNode = 5000, minInformationGain = 0.0)
print(dtModel)

# evaluate model using r2 
# # fitted model Rsquared calcuation R2 = ssreg / sstot
dtR2 <- adatao.r2(model = dtModel, data = trainingData)
dtFittedData <- adatao.predict(dtModel, trainingData)
dtFitted_df = fetchRows(dtFittedData , nrow(dtFittedData))
expect_equal( dtR2, sum((dtFitted_df$yPredict - mean(dtFitted_df$ytrue))^2) / sum((dtFitted_df$ytrue - mean(dtFitted_df$ytrue))^2)  )


# make prediction
dtPredData <- adatao.predict(dtModel, testData)

# visualize a sample of predicted data
sampledtPred = fetchRows(dtPredData, 100)
plot(x=sampledtPred$ytrue, y=sampledtPred$yPredict)

# evaluate model using mse on test data
dtMse <- adatao.mse(model=dtModel, data=testData)
dtPred_df = fetchRows(dtPredData , nrow(dtPredData))
expect_equal(sqrt(dtMse),sqrt(mean((dtPred_df$ytrue - dtPred_df$yPredict)^2)))


# --- test RF model --- featureSubsetStrategy = 'auto'
rfModel <- adatao.randomForest(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32, numTrees = 20, featureSubsetStrategy = 'auto', minInstancePerNode = 5000, minInformationGain = 0.0, seed = 0)
print(rfModel)
# make prediction on testData
rfPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleRfPred = fetchRows(rfPredData, 100)
plot(x=sampleRfPred$ytrue, y=sampleRfPred$yPredict)

# evaluate model using mse on test data
rfMse <- adatao.mse(model=rfModel, data=testData)
RfPred_df = fetchRows(rfPredData , nrow(rfPredData))
expect_equal(sqrt(rfMse),sqrt(mean((RfPred_df$ytrue - RfPred_df$yPredict)^2)))


# --- test RF model --- featureSubsetStrategy = 'all'
rfModel <- adatao.randomForest(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32, numTrees = 50, featureSubsetStrategy = 'all', minInstancePerNode = 5000, minInformationGain = 0.0, seed = 0)
print(rfModel)
# make prediction on testData
rfPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleRfPred = fetchRows(rfPredData, 100)
plot(x=sampleRfPred$ytrue, y=sampleRfPred$yPredict)

# evaluate model using mse on test data
rfMse <- adatao.mse(model=rfModel, data=testData)
RfPred_df = fetchRows(rfPredData , nrow(rfPredData))
expect_equal(sqrt(rfMse),sqrt(mean((RfPred_df$ytrue - RfPred_df$yPredict)^2)))


# --- test RF model --- featureSubsetStrategy = 'sqrt'
rfModel <- adatao.randomForest(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32, numTrees = 100, featureSubsetStrategy = 'sqrt', minInstancePerNode = 5000, minInformationGain = 0.0, seed = 0)
print(rfModel)
# make prediction on testData
rfPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleRfPred = fetchRows(rfPredData, 100)
plot(x=sampleRfPred$ytrue, y=sampleRfPred$yPredict)

# evaluate model using mse on test data
rfMse <- adatao.mse(model=rfModel, data=testData)
RfPred_df = fetchRows(rfPredData , nrow(rfPredData))
expect_equal(sqrt(rfMse),sqrt(mean((RfPred_df$ytrue - RfPred_df$yPredict)^2)))


# --- test RF model --- featureSubsetStrategy = 'log2'
rfModel <- adatao.randomForest(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32, numTrees = 100, featureSubsetStrategy = 'log2', minInstancePerNode = 5000, minInformationGain = 0.0, seed = 0)
print(rfModel)
# make prediction on testData
rfPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleRfPred = fetchRows(rfPredData, 100)
plot(x=sampleRfPred$ytrue, y=sampleRfPred$yPredict)

# evaluate model using mse on test data
rfMse <- adatao.mse(model=rfModel, data=testData)
RfPred_df = fetchRows(rfPredData , nrow(rfPredData))
expect_equal(sqrt(rfMse),sqrt(mean((RfPred_df$ytrue - RfPred_df$yPredict)^2)))

# --- test RF model --- featureSubsetStrategy = 'onethird'
rfModel <- adatao.randomForest(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32, numTrees = 200, featureSubsetStrategy = 'onethird', minInstancePerNode = 5000, minInformationGain = 0.0, seed = 0)
print(rfModel)
# make prediction on testData
rfPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleRfPred = fetchRows(rfPredData, 100)
plot(x=sampleRfPred$ytrue, y=sampleRfPred$yPredict)

# evaluate model using mse on test data
rfMse <- adatao.mse(model=rfModel, data=testData)
RfPred_df = fetchRows(rfPredData , nrow(rfPredData))
expect_equal(sqrt(rfMse),sqrt(mean((RfPred_df$ytrue - RfPred_df$yPredict)^2)))


# ---- test GBT model --- lossFn = "SquaredError"
gbtModel <- adatao.gradientBoostedTrees(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32,  numIterations = 50,  learningRate = 0.1, lossFn = "SquaredError", minInstancePerNode = 5000, minInformationGain = 0.0)
print(gbtModel)
# make prediction
gbtPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleGbtPred = fetchRows(gbtPredData, 100)
plot(x=sampleGbtPred$ytrue, y=sampleGbtPred$yPredict)

# evaluate model using mse on test data
gbtMse <- adatao.mse(model=gbtModel, data=testData)
gbtPred_df = fetchRows(gbtPredData , nrow(gbtPredData))
expect_equal(sqrt(gbtMse),sqrt(mean((gbtPred_df$ytrue - gbtPred_df$yPredict)^2)))


# ---- test GBT model --- lossFn = "LogLoss"
gbtModel <- adatao.gradientBoostedTrees(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32,  numIterations = 200, lossFn = "LogLoss",  learningRate = 0.001, minInstancePerNode = 5000, minInformationGain = 0.0)
print(gbtModel)
# make prediction
gbtPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleGbtPred = fetchRows(gbtPredData, 100)
plot(x=sampleGbtPred$ytrue, y=sampleGbtPred$yPredict)

# evaluate model using mse on test data
gbtMse <- adatao.mse(model=gbtModel, data=testData)
gbtPred_df = fetchRows(gbtPredData , nrow(gbtPredData))
expect_equal(sqrt(gbtMse),sqrt(mean((gbtPred_df$ytrue - gbtPred_df$yPredict)^2)))


# ---- test GBT model --- lossFn = "AbsoluteError"
gbtModel <- adatao.gradientBoostedTrees(regression_model, data=trainingData, method = 'regression', impurity = 'Variance', maxDepth = 10, maxBin = 32,  numIterations = 100,  learningRate = 0.01, lossFn = "AbsoluteError", minInstancePerNode = 5000, minInformationGain = 0.0)
print(gbtModel)
# make prediction
gbtPredData <- adatao.predict(rfModel, testData)

# visualize a sample of predicted data
sampleGbtPred = fetchRows(gbtPredData, 100)
plot(x=sampleGbtPred$ytrue, y=sampleGbtPred$yPredict)

# evaluate model using mse on test data
gbtMse <- adatao.mse(model=gbtModel, data=testData)
gbtPred_df = fetchRows(gbtPredData , nrow(gbtPredData))
expect_equal(sqrt(gbtMse),sqrt(mean((gbtPred_df$ytrue - gbtPred_df$yPredict)^2)))








adatao.disconnect()
})

