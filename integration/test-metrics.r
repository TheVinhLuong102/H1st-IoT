#######################################################
# (c) Copyright 2013, Adatao, Inc. All Rights Reserved.

library(adatao)
context("Metrics")

test_that("Confusion matrix for glm works on SharkDataFrame", {
  
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists admission")
  adatao.sql("CREATE TABLE admission (admit int, gre int, gpa float, rank int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/admission.csv' INTO TABLE admission")
  df<- adatao.loadHiveTable("admission")
  
  df <- adatao.as.factor(df, "admit")
  
  glm <- adatao.glm.gd(admit ~ gpa, data=df, learningRate=0.1, numIterations=50, initialWeights=c(-4.6,1.5))
  
  cf <- adatao.binary.confusion.matrix(model=glm,data=df)
  
  expect_equivalent(cf, matrix(c(0,127,0,273),ncol=2, byrow=T))
  
  # regression test for ~ . formula
  glm <- adatao.glm(admit ~ ., data=df)
  cf <- adatao.binary.confusion.matrix(model=glm,data=df)
  expect_equivalent(cf, matrix(c(58,196,40,506),ncol=2, byrow=T))
  
  
  adatao.disconnect()
})

test_that("Confustion matrix works with normal DataFrame", {
  adatao.connect("localhost")
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  
  glm <- adatao.glm.gd(V1 ~ V3, data=df, learningRate=0.1, numIterations=50, initialWeights=c(-4.6,1.5))
  
  cf <- adatao.binary.confusion.matrix(model=glm,data=df)
  
  expect_equivalent(cf, matrix(c(0,127,0,273),nrow=2, byrow=T))
  
  adatao.disconnect()
})

test_that("Test decision tree", {
  
  #adatao.connect("54.197.142.178", 7911)
  
  adatao.connect("54.242.89.92")
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists admission")
  adatao.sql("CREATE TABLE admission (admit int, gre int, gpa float, rank int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/admission.csv' INTO TABLE admission")
  
  df <- adatao.sql2ddf("select * from admission")
  df <- adatao.as.factor(df, "admit")
  
  
  dtmodel <- adatao.decisionTree(admit ~ gre + gpa,  data=df, impurity="gini", method="Classification", maxDepth=2)
  
  print(dtmodel)
  
  #cf <- adatao.roc(model=dtmodel,ddf=df)
  prediction <- adatao.predict(dtmodel, data=df)
  
  metric <- adatao.metrics(data=prediction, alpha_length=100)
  
  r2 <- adatao.r2(dtmodel, df)
  
  data <- data.frame(tpr=metric$tpr, fpr=metric$fpr)
  Line2 <- gvisLineChart(data, xvar="fpr", yvar="tpr",
                         options=list(title="ROC",
                                      titleTextStyle="{color:'red',fontName:'Courier',fontSize:16}",
                                      curveType='function'))
  adatao.viz.show(Line2)
  
  
  adatao.disconnect()
})