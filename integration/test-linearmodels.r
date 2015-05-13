#######################################################
# (c) Copyright 2013, Adatao, Inc. All Rights Reserved.

library(adatao)
context("Linear Models")

test_that("Normal Equation Linear Regression works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  result <- adatao.lm(V1 ~ V6, data=df)
  
  expect_identical(paste0(format(result$coefficients),collapse=","), "37.285126,-5.344472")
  expect_identical(paste0(format(result$stderrs), collapse=","), "1.877627,0.559101")
  expect_identical(paste0(format(result$rss), collapse=","), "278.3219")
  expect_identical(paste0(format(result$sst), collapse=","), "1126.047")
  expect_equal(result$numSamples, 32)
  expect_equal(result$nfeatures, 1)
  expect_equal(result$vif, NULL)
  expect_equal(paste(format(adatao.quantile(result$residuals)), collapse=","), "-4.543151,-2.611004,-0.200144, 1.297350, 6.872711")
  
  result2 <- adatao.lm(V1 ~ ., data=df)
  expect_equal(result2$nfeatures, 10)
  expect_identical(paste(names(result2$coefficients), collapse=" "), "(Intercept) V2 V3 V4 V5 V6 V7 V8 V9 V10 V11")
  adatao.disconnect()
  
  })

test_that("Normal Equation Linear Regression - multiple variables works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  result <- adatao.lm(V1 ~ V4 + V6, data=df)
  adatao.disconnect()
  
  expect_identical(paste0(format(result$coefficients),collapse=","), "37.22727012,-0.03177295,-3.87783074")
  expect_identical(paste0(format(result$stderrs), collapse=","), "1.59878754,0.00902971,0.63273349")
  expect_identical(paste0(format(result$rss), collapse=","), "195.0478")
  expect_identical(paste0(format(result$sst), collapse=","), "1126.047")
  expect_equal(result$numSamples, 32)
  expect_equal(result$nfeatures, 2)
  expect_equal(paste0(format(result$vif), collapse=","), "1.766625,1.766625")
})

test_that("Linear Regression Normal Equation categorical on SharkDataFrame works", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists airline")
  adatao.sql("create table airline (years bigint, v2 double, v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 string, v10 double, v11 string, v12 double, v13 double, v14 double, v15 double, v16 double, airport string, v18 string, v19 double, v20 double, v21 double, v22 double, v23 double, v24 double, v25 double, v26 double, v27 double, v28 double, v29 double) row format delimited fields terminated by ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  df <- adatao.loadHiveTable(table_name="airline")
  
  model <- adatao.lm(years ~ airport + v18, data=df)
  # this model cannot be solved by solvePositive() which uses Cholesky
  # the error is 
  # Error in executingLinearRegressionNormalEquation LAPACK DPOSV: Leading minor of order i of A is not positive definite.
  # it cannot be solved by solve() or solveSymmetric()
  # the error is
  # Error in executingLinearRegressionNormalEquation LAPACK SYV: Linear equation cannot be solved because the matrix was singular.
  # one solution is to use ridge regression with lambda > 0
  # however, the resulted model is still not OK :D
  # even after remove v3 in the formula (v3 has all values 3), its still not OK
  # the reason is that there are duplicate rows, which makes the design matrix not full-row rank, 11/15
  # even after remove duplicate rows in design matrix (airport, v18) 11/13
  
  adatao.disconnect()
})

test_that("Linear Regression Normal Equation categorical on SharkDataFrame works", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists mtcars")
  adatao.sql("CREATE TABLE mtcars (mpg double, cyl int, disp double, hp int, drat double, wt double, qesc double, vs int, am int, gear int, carb string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/mtcars' INTO TABLE mtcars")
  df <- adatao.loadHiveTable(table_name="mtcars")
  df2 <- adatao.as.factor(df,cols="vs")
  
  result <- adatao.lm(mpg ~ hp + wt + vs, data=df2)
  s <- summary(result)
  expect_equivalent(paste0(format(s$coef_table$`t value`), collapse=","),"22.054365,-2.311667,-5.907677,-1.010901")
  expect_equivalent(paste0(format(s$coef_table$`Pr(>|t|)`), collapse=","),"3.075148e-19,2.837035e-02,2.346759e-06,3.207205e-01")
  expect_equivalent(paste0(format(s$res.stderr), collapse=","),"2.592432")
  expect_equivalent(paste0(format(s$r2), collapse=","),"0.8328847")
  expect_equivalent(paste0(format(s$r2.adjusted), collapse=","),"0.8149795")
  expect_equivalent(paste0(format(s$fstatistic), collapse=","),"4.651633e+01,3.000000e+00,2.800000e+01,5.275692e-11")
  
  # R summary(lm()) has the same numbers except the intercept coefficients numbers
  # ours
  #              Estimate  Std. Error  t value   Pr(>|t|)
  #(Intercept)  36.75038      1.6664   22.054  3.075e-19
  # R's
  #            Estimate Std. Error t value Pr(>|t|)    
  #(Intercept) 35.38267    2.42564  14.587 1.31e-14
  
  df2 <- adatao.cut(x=df, column="drat", breaks=3, include.lowest=T)
  
  result <- adatao.lm(mpg ~ drat, data=df2)
  
  df2 <- adatao.as.factor(df2,cols="carb")
  result <- adatao.lm(mpg ~ carb + drat, data=df2)
})


test_that("Linear Regression works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  result <- adatao.lm.gd(V1 ~ V4 + V6, data=df, learningRate=0.00005, numIterations=10, initialWeights=c(37.3, -0.04, -4))
  adatao.disconnect()
  #nhan's one
  expect_identical(paste0(format(result$weights),collapse=","), "37.30007207,-0.02977558,-3.99973618")
  #nhan: 
  #Khang: this is kind of unnecessary as given the weight is correct then training errors whould be correct.
  expect_equal(paste0(format(result$rmse[1:10]),collapse=","), "3.179693,3.065195,3.054606,3.053626,3.053534,3.053525,3.053524,3.053523,3.053522,3.053522")
})

test_that("Linear Regression works on SharkDataFrame", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists mtcars")
  adatao.sql("CREATE TABLE mtcars (mpg double, cyl int, disp double, hp int, drat double, wt double, qesc double, vs int, am int, gear int, carb int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/mtcars' INTO TABLE mtcars")
  df <- adatao.loadHiveTable(table_name="mtcars")
  result <- adatao.lm.gd(mpg ~ hp + wt, data=df, learningRate=0.00005, numIterations=10, initialWeights=c(37.3, -0.04, -4))
  adatao.disconnect()
  expect_identical(paste0(result$weights,collapse=","), "37.3000720710625,-0.0297755836949357,-3.99973618291579")
})

test_that("Ridge Regression works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  lm <- adatao.lm.gd(V1 ~ V4 + V6, data=df, learningRate=0.00005, numIterations=10, regularized="ridge", lambda=1, initialWeights=c(37.3, -0.04, -4))
  adatao.disconnect()
  #nhan
  expect_identical(paste0(format(lm$weights),collapse=","), "37.29878996,-0.02977133,-3.99959856")
})

test_that("Ridge Regression works on SharkDataFrame", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists mtcars")
  adatao.sql("CREATE TABLE mtcars (mpg double, cyl int, disp double, hp int, drat double, wt double, qesc double, vs int, am int, gear int, carb int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/mtcars' INTO TABLE mtcars")
  df <- adatao.loadHiveTable(table_name="mtcars")
  result <- adatao.lm.gd(mpg ~ hp + wt, data=df, learningRate=0.00005, numIterations=10, regularized="ridge", lambda=1, initialWeights=c(37.3, -0.04, -4))
  adatao.disconnect()
  expect_identical(paste0(result$weights,collapse=","), "37.2987899645143,-0.0297713292108673,-3.99959856462058")
})

test_that("Logistic Regression IRLS works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/flu.table.noheader",sep=" ")
  result <- adatao.glm(V1 ~ V2 + V3, data=df, family=binomial())
  s <- summary(result)
  adatao.disconnect()
  expect_identical(result$iter, 6)
  expect_identical(result$numSamples, 50)
  
  expect_identical(paste0(format(s$coef_table$`z value`),collapse=","), "-3.363471, 2.982934, 3.244558")
  expect_identical(paste0(format(s$coef_table$Estimate),collapse=","), "-21.5845817,  0.2217768,  0.2035069")
  expect_identical(paste0(format(s$coef_table$`Std. Error`),collapse=","), "6.41735421,0.07434853,0.06272252")
  expect_identical(paste0(format(s$aic),collapse=","), "38.41631")
  expect_identical(paste0(format(s$deviance),collapse=","), "32.41631")
  expect_identical(paste0(format(s$null.deviance),collapse=","), "68.0292")
})

test_that("Logistic Regression sparse works", {
  
  adatao.connect("localhost", 7911)
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists admission")
  adatao.sql("CREATE TABLE admission (V1 DOUBLE, V2 DOUBLE, V3 DOUBLE, V4 int) row format delimited fields terminated by ' '")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/admission2.csv' INTO TABLE admission")
  df <- adatao.loadHiveTable(table_name="admission")
  summary(df)
  
  df4 <- adatao.as.factor(df,cols=c("v2","v4"), isBigFactor=FALSE)
  
  glm1 <- adatao.glm.gd.sparse(v1 ~ v2 + v4, data=df4, learningRate=0.1, numIterations=1, initialWeights=c(-4.6,1.5,1))
  
  adatao.disconnect()
  # maes
  ##expect_equal(paste0(lm$maes,collapse=","), "2167505232143596,8.91915207447969e+24,3.67016597351294e+34,1.51024650752839e+44,6.21455413723033e+53,2.55724366400103e+63,1.05228710099996e+73,4.33008460835686e+82,1.78179820865539e+92,7.33196956530672e+101")
})

test_that("Logistic Regression sparse for string columns", {
  
  adatao.connect("localhost", 7911)
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists airline")
  adatao.sql("create table airline (years bigint, v2 double, v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 string, v10 double, v11 string, v12 double, v13 double, v14 double, v15 double, v16 double, airport string, v18 string, v19 double, v20 double, v21 double, v22 double, v23 double, v24 double, v25 double, v26 double, v27 double, v28 double, v29 double) row format delimited fields terminated by ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  #df <- adatao.loadHiveTable(table_name="airline")
  df <- adatao.sql2ddf("select if(v2 > 5, 1, 0) as v2 , v3, v11 from airline")
  summary(df)
  
  df4 <- adatao.as.factor(df,cols=c("v11"), isBigFactor=TRUE)
  
  glm1 <- adatao.glm.gd.sparse(v2 ~ v3 + v11, data=df4, learningRate=0.1, numIterations=1, initialWeights=c(-4.6,1.5,1))
  glm1
  
  adatao.disconnect()
  # maes
  ##expect_equal(paste0(lm$maes,collapse=","), "2167505232143596,8.91915207447969e+24,3.67016597351294e+34,1.51024650752839e+44,6.21455413723033e+53,2.55724366400103e+63,1.05228710099996e+73,4.33008460835686e+82,1.78179820865539e+92,7.33196956530672e+101")
})

test_that("test join", {
  
  adatao.connect("localhost", 7911)
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists airline")
  adatao.sql("create table airline (years bigint, v2 double, v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 string, v10 double, v11 string, v12 double, v13 double, v14 double, v15 double, v16 double, airport string, v18 string, v19 double, v20 double, v21 double, v22 double, v23 double, v24 double, v25 double, v26 double, v27 double, v28 double, v29 double) row format delimited fields terminated by ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  df <- adatao.loadHiveTable(table_name="airline")
  
  temptable <- "anotherTable"
  origintable <- "airline"
  stringcolumn <- "v9"
  
  adatao.sql("create temporary function row_sequence as 'org.apache.hadoop.hive.contrib.udf.UDFRowSequence'")
  adatao.sql(paste("drop table",temptable))
  adatao.sql(paste("create table ",temptable, "(id Int, ", stringcolumn, " string)"))
  
  adatao.sql(paste("INSERT INTO TABLE ", anotherTable," SELECT row_sequence(), ", stringcolumn, " from ", origintable))
  
  df2 <- adatao.sql2ddf(paste("select * from ",anotherTable))
  summary(df2)
  
  df3 <- adatao.join(df, df2, by=c(stringcolumn))
  
  #replace column v9 by column r_id
  formula <- "v1 ~ v3 + v9"
  newformular <- gsub(stringcolumn, "r_id", formula)
  
  summary(df3)
  
  adatao.disconnect()
  # maes
  ##expect_equal(paste0(lm$maes,collapse=","), "2167505232143596,8.91915207447969e+24,3.67016597351294e+34,1.51024650752839e+44,6.21455413723033e+53,2.55724366400103e+63,1.05228710099996e+73,4.33008460835686e+82,1.78179820865539e+92,7.33196956530672e+101")
})

test_that("Logistic Regression IRLS works", {  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  result <- adatao.glm(V1 ~ V3, data=df, family=binomial())
  s <- summary(result)
  adatao.disconnect()
  
  expect_identical(result$iter, 4)
  expect_identical(result$numSamples, 400)
  
  expect_identical(paste0(format(s$coef_table$`z value`),collapse=","), "-4.208944, 3.516953")
  expect_identical(paste0(format(s$coef_table$Estimate),collapse=","), "-4.357587, 1.051109")
  expect_identical(paste0(format(s$coef_table$`Std. Error`),collapse=","), "1.0353161,0.2988691")
  expect_identical(paste0(format(s$aic),collapse=","), "490.9676")
  expect_identical(paste0(format(s$deviance),collapse=","), "486.9676")
  expect_identical(paste0(format(s$null.deviance),collapse=","), "499.9765")
})

test_that("Logistic Regression works", {
  
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/admission.csv",sep=" ")
  lm <- adatao.glm.gd(V1 ~ V3, data=df, learningRate=0.1, numIterations=50, initialWeights=c(-4.6,1.5))
  adatao.disconnect()
  expect_identical(paste0(lm$weights,collapse=","), "-4.69750205604402,1.14870572125879")
  # maes
  ##expect_equal(paste0(lm$maes,collapse=","), "2167505232143596,8.91915207447969e+24,3.67016597351294e+34,1.51024650752839e+44,6.21455413723033e+53,2.55724366400103e+63,1.05228710099996e+73,4.33008460835686e+82,1.78179820865539e+92,7.33196956530672e+101")
})


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

#unit test of lm categorical
test_that("Linear Regression categorical on SharkDataFrame", {
  adatao.connect("localhost", 7911)
  
  adatao.sql("set shark.test.data.path=resources")
  adatao.sql("drop table if exists airline")
  adatao.sql("create table airline (years bigint, v2 double, v3 double, v4 double, v5 double, v6 double, v7 double, v8 double, v9 string, v10 double, v11 string, v12 double, v13 double, v14 double, v15 double, v16 double, airport string, v18 string, v19 double, v20 double, v21 double, v22 double, v23 double, v24 double, v25 double, v26 double, v27 double, v28 double, v29 double) row format delimited fields terminated by ','")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/airline.csv' INTO TABLE airline")
  df <- adatao.loadHiveTable(table_name="airline")
  
  model <- adatao.lm.gd(years ~ airport + v3 + v18, data=df, learningRate=0.00005, numIterations=10, ref.levels=list(v18="LAS"))
  expect_identical(unlist(attributes(model$weights))[[3]], "airportIAD")
  expect_equal(length(model$weights), 12)
  # ref levels
  expect_false("v18LAS" %in% names(model$weights))
  
  model <- adatao.lm.gd(years ~ airport + v3 + v18, data=df, learningRate=0.00005, numIterations=10, ref.levels=list(v18="LAS", airport="IAD"))
  expect_false("airportIAD" %in% names(model$weights))
  
  model <- adatao.lm(years ~ airport + v3 + v18, data=df, ref.levels=list(v18="LAS", airport="IAD"))
  expect_equal(length(model$coefficients), 12)
  # ref levels
  expect_false("v18LAS" %in% names(model$coefficients))
  expect_false("airportIAD" %in% names(model$coefficients))
  
  adatao.disconnect()
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

test_that("Decision Tree", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  result <- adatao.rpart(V1 ~ V6, data=df)
  adatao.disconnect()
  
})

