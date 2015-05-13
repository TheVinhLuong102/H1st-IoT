#######################################################
# (c) Copyright 2013, Adatao, Inc. All Rights Reserved.

library(adatao)
context("Linear Models")

createDemoTables <- function() {
  adatao.connect("localhost", 7911)
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists admission")
  adatao.sql("CREATE TABLE admission (V1 DOUBLE, V2 DOUBLE, V3 DOUBLE, V4 DOUBLE) row format delimited fields terminated by ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/admission2.csv' INTO TABLE admission")
  df <- adatao.loadHiveTable(table_name="admission")
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists mtcars")
  adatao.sql("CREATE TABLE mtcars (mpg double, cyl int, disp double, hp int, drat double, wt double, qesc double, vs int, am int, gear int, carb int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/mtcars' INTO TABLE mtcars")
  df <- adatao.loadHiveTable(table_name="mtcars")

  adatao.sql("create table airline (Year int,Month int,DayofMonth int, DayOfWeek int,DepTime int, CRSDepTime int,ArrTime int, CRSArrTime int,UniqueCarrier string, FlightNum int, TailNum string, ActualElapsedTime int, CRSElapsedTime int, AirTime int, ArrDelay int, DepDelay int, Origin string, Dest string, Distance int, TaxiIn int, TaxiOut int, Cancelled int, CancellationCode string, Diverted string, CarrierDelay int, WeatherDelay int, NASDelay int, SecurityDelay int, LateAircraftDelay int ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  
  df <- adatao.loadHiveTable(table_name="airline")
  
  adatao.disconnect()
}

demo("Demo pa-ddf") {
  createDemoTables()
  adatao.connect("localhost", 7911)
  
  #Load data, SQL2 dataframe
  ddf <- adatao.sql2ddf("select * from mtcars")
  
  #Metadata
  ddf@env$colnames #column names
  nrow(ddf)
  fetchRows(ddf,3)

  
  #Basic Stats
  summary(ddf)
  #TODO: fix this
  a <- adatao.fivenum(ddf)
  
  #TODO migrate aggregation
  
  #rdf_mean2 <- adatao.aggregate(cbind(mpg,disp) ~ vs, ddf, FUN=mean)
  #expect_true((rdf_mean2[1,"mpg"] - 24.55714)<=1e-5)
  #rdf_median <- adatao.aggregate(cbind(mpg,disp) ~ vs, ddf, FUN=median)
  #expect_true((rdf_median[1,"mpg"] - 22.15)<=1e-2)
  #rdf_variance <- adatao.aggregate(cbind(mpg,disp) ~ vs, ddf, FUN=var)
  #expect_true((rdf_median[1,"mpg"] - 26.86673)<=1e-5)
  #rdf_summary <- adatao.aggregate(cbind(mpg,disp) ~ vs, ddf, FUN=summary)
  #expect_identical(paste0(rdf_summary[1,],collapse=","), "1,17.8,33.9,22.15,20.3,28.075,71.1,258,120.1,78.85,151.925")
  #rdf_mean3 <- adatao.aggregate(cbind(mpg,disp) ~ vs + vs + drat, ddf, FUN=mean)
  #expect_identical(paste(names(rdf_mean3), collapse=","), "vs,drat,mpg,disp")
  #expect_true(is.integer(rdf_mean3$vs))
  #expect_true(is.double(rdf_mean3$drat))
  
  #TODO fix (Diagnostic message: Only support numeric verctors!!!), need to migrate vector quantile to support DDF
  adatao.quantile(ddf$mpg)
  
  
  #xtabs
  x <- adatao.xtabs(mpg~hp+vs, ddf, exclude=NULL, na.action=na.pass)
  y <- adatao.xtabs(~hp + vs, ddf)
  z <- adatao.xtabs(~ ncontrols, ddf)
  
  
  #subset
  df <- ddf[,c("mpg", "hp")] # column projection
  summary(df)
  v <- df$mpg
  expect_is(v, "AdataoVector")
  rows <- fetchRows(df, limit=10)
  rows
  
  #as.factor
  df2 <- adatao.as.factor(ddf,cols=c("mpg","hp"))
  df2
  
  
  
  
  
  #===================demo 1
  #linear regression one variable
  result <- adatao.lm(v1 ~ v6, data=df)
  #expect_identical(paste0(format(result$coefficients),collapse=","), "37.285126,-5.344472")
  expect_equal(result$numSamples, 32)
  expect_equal(result$nfeatures, 1)
  expect_equal(result$vif, NULL)
  
  #this doesn't work, please check, Cuong
  # the parameter of quantile must be a DDF vector.
  # result residuals is just a normal R vector
  expect_equal(paste(format(adatao.quantile(result$residuals)), collapse=","), "-4.543151,-2.611004,-0.200144, 1.297350, 6.872711")
  
  
  nrow(df)
  
  #====================demo 2
  prediction2 <- adatao.predict(model=result, data=df)
  adatao.r2(model=result, data=df)
  
  #metric residual
  adatao.residuals(result)
  
  
  
  #=====================demo 3
  #lm on multiple variables
  df <- adatao.sql2ddf("select v4, v6, v1 from mtcars")
  result <- adatao.lm(v1 ~ v4 + v6, data=df)
  
  
  #=====================demo 4
  #logistic regression GD
  result <- adatao.lm.gd(v1 ~ v4 + v6, data=df, learningRate=0.00005, numIterations=10, initialWeights=c(37.3, -0.04, -4))
  
  #=====================demo 5
  #cut, doesnt work on representation handler
  df2 <- adatao.cut(x=df, column="v4", breaks=3, include.lowest=T)
  result <- adatao.lm(v1 ~ v4, data=df2)
  
  #bug on factor column
  df2 <- adatao.as.factor(df2,cols="v4")
  result <- adatao.lm(v1 ~ v4 + v6, data=df2)
  
  #=====================demo 6
  #logistic regression gd
  df <- adatao.sql2ddf("select v3, v4, v1 from admission")
  glm1 <- adatao.glm.gd(v1 ~ v3 + v4, data=df, learningRate=0.1, numIterations=1, initialWeights=c(-4.6,1.5, 1))
  
  
  #=====================demo 6
  #prediction
  prediction1 <- adatao.predict(model=glm1, data=df)
  
  #=====================demo 7
  #doesnt work yet, maybe because of prediction1
  result <- adatao.metrics(data=prediction1)
  
  adatao.binary.confusion.matrix(model=glm1, data=df, threshold=0.5)
  
}


demo_ckb("Demo pa-ddf vector quantiles, confusion matrix") {
  createDemoTables()
  adatao.connect("localhost", 7911)
  ddf <- adatao.sql2ddf("select distance, depdelay, if (arrdelay > 10.89, 1, 0) as delayed from airline")
  # vector quantil, need to project a DDF to one single column to make a DDF vector
  v1 = ddf[c("distance")]
  adatao.quantile(v1)
  delay_model <- adatao.glm.gd(delayed ~ distance + depdelay, ddf, learningRate=1, numIterations=20)
  adatao.binary.confusion.matrix(delay_model, ddf, 0.5)

  ddf <- adatao.sql2ddf("select distance, depdelay, arrdelay from airline")
  delay_model <- adatao.lm.gd(arrdelay~distance + depdelay, ddf, learningRate=1, numIterations=20)

  adatao.binary.confusion.matrix(delay_model, ddf, 0.5)

  delay_model <- adatao.lm(arrdelay~distance + depdelay, ddf)

  adatao.binary.confusion.matrix(delay_model, ddf, 0.5)

  # Kmeans
  km <- adatao.kmeans(ddf, cols=c("distance", "depdelay", "arrdelay"), numClusters=3, numIters=5)

}

test_that("ROC for classification glm", {
  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  model <- adatao.glm.gd(V1 ~ V3, data=df, learningRate=0, numIterations=50, initialWeights=c(-4,1))
  #load test file
  df.test<-adatao.loadTable("resources/admission.csv",sep=" ")
  prediction <- adatao.predict(model, df.test)
  
  #call ROC
  metric <- adatao.metrics(data=prediction, alpha_length=10)
  
  expect_identical(format(metric$auc),"0.6132144")
  
  adatao.disconnect()
  
})

test_that("ROC/metrics for randomforest", {
  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  
  #model random forest
  rrf <- adatao.randomForest(V1 ~ V3 , data=df, ntree=5, userSeed=10)
  str(rrf)
  
  #load test file
  df.test<-adatao.loadTable("resources/admission.csv",sep=" ")
  #prediction
  prediction <- adatao.predict(rrf, df.test)
  
  #call ROC
  metric <- adatao.metrics(data=prediction, alpha_length=10)
  
  adatao.disconnect()
  
})


test_that("Logistic Regression multiple vars works", {
  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  lm <- adatao.glm.gd(V1 ~ V3 + V4, data=df, learningRate=0.1, numIterations=40, initialWeights=c(-3, 1.5, -0.9))
  adatao.disconnect()  
  # weights
  expect_identical(paste0(lm$weights,collapse=","),"-3.06164528167647,1.26306761815179,-0.851416849831873")
})

test_that("Logistic Regression airline delay works", {
  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/airline-transform.3.csv",sep=",")
  
  lm <- adatao.glm.gd(V13 ~ V5 + V6 , data=df, learningRate=0.1, numIterations=10, initialWeights=c(-2, 48, -47))
  adatao.disconnect()
  # weights
  expect_identical(paste0(lm$weights,collapse=","), "-2.16985861316207,47.7368575162061,-47.2607852023823")
  
})


test_that("Logistic Regression for categorical and int column on SharkDataFrame", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists airline")
  adatao.sql("create table airline (years bigint, v2 double, v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 string, v10 double, v11 string, v12 double, v13 double, v14 double, v15 double, v16 double, airport string, v18 string, v19 double, v20 double, v21 double, v22 double, v23 double, v24 double, v25 double, v26 double, v27 double, v28 double, v29 double) row format delimited fields terminated by ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  df <- adatao.sql2ddf("select years, v3, airport, v18, v22, v5 from airline")
  df2 <- adatao.as.factor(df,cols=c("years","airport"))
  
  model <- adatao.glm.gd(v22 ~ years + v3 , data=df2, learningRate=0.00005, numIterations=10, ref.levels=list(years="2010"))
  
  expect_equal(length(model$weights), 4)
  # ref levels
  expect_true(names(df2@env$colfactors$years)[[3]]=="2010")
  expect_false("years2010" %in% names(model$weights))
  
  model <- adatao.glm.gd(v22 ~ years + v3 , data=df, learningRate=0.00005, numIterations=10)
  # ref levels
  expect_false("years2008" %in% names(model$weights))
  
  model <- adatao.glm(v22 ~ airport, data=df, ref.levels=list(airport="IAD"))
  expect_false("airportIAD" %in% names(model$coefficients))
  
  #df2 <- adatao.as.factor(df,cols=list("v5"))
  # singular!!!
  # model2 <- NULL
  # model2 <- adatao.glm(v22 ~ v5 , data=df2)
  # expect_true(!is.null(model2))
  
  adatao.disconnect()
})

test_that("adatao.fitted works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  model.fitted <- adatao.lm(V1 ~ V6, data=df)
  dfit <- adatao.fitted(model.fitted)
  bdfit <- fetchRows(dfit, 1)
  expect_identical(paste0(format(bdfit[1,]),collapse=","), "21,23.28261")
  adatao.disconnect()
})

test_that("adatao.residuals works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  model.res <- adatao.lm(V1 ~ V6, data=df)
  v <- adatao.residuals(model.res)
  fv <- fetchVector(v, 1)
  expect_identical(format(fv[1]), "-2.282611")
  
  model <- adatao.lm.gd(V1 ~ V4 + V6, data=df, learningRate=0.00005, numIterations=10, initialWeights=c(37.3, -0.04, -4))
  v <- adatao.residuals(model)
  fv <- fetchVector(v, 1)
  expect_identical(format(fv[1]), "-2.545449")
  adatao.disconnect()
  
})


test_that("Huan's work") {
  adatao.connect()
  ddf <- adatao.sql2ddf("select * from airline")
  factor <- adatao.as.factor(ddf, c("year", "month", "dayofmonth"))
  
  lm_model <- adatao.lm(arrdelay ~ month + dayofmonth, ddf)
  ytrue_ypred <- adatao.predict(lm_model, ddf)
  
  ddf2 <- adatao.sql2ddf("select month, dayofmonth, arrdelay from airline")
  adatao.cv.lm(arrdelay ~ month + dayofmonth, ddf2)
}

