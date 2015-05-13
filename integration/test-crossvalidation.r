library(adatao)
context("Cross Validation")

adatao.connect("localhost", 7911)

df1 <-adatao.loadTable("resources/mtcars",sep=" ")


adatao.sql("set shark.test.data.path=resources")

adatao.sql("drop table if exists mtcars")
adatao.sql("CREATE TABLE mtcars (mpg double, cyl int, disp double, hp int, drat double, wt double, qesc double, vs int, am int, gear int, carb int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/mtcars' INTO TABLE mtcars")
df2 <- adatao.loadHiveTable(table_name="mtcars")

adatao.sql("drop table if exists admission")
adatao.sql("CREATE TABLE admission (V1 int, V2 int, V3 double, V4 int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '")
adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/admission.csv' INTO TABLE admission")
df3 <- adatao.loadHiveTable(table_name="admission")

test_that("KFold works on normal DataFrame", {
  kfold_list <- adatao.cv.kfold(data=df1,nFolds=2,seed=17)
  expect_equal(length(kfold_list),2)
  expect_equal(length(kfold_list[[1]]),2)
  expect_equal(length(kfold_list[[2]]),2)
})

test_that("KFold works on normal DataFrame with factor columns", {
  # regression test
  df12 <- adatao.as.factor(df1, "V8")
  kfold_list <- adatao.cv.kfold(data=df12,nFolds=2,seed=17)
  expect_identical(paste0(names(kfold_list[[1]]$train@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(kfold_list[[1]]$train@env$colfactors$V8, collapse=","),"8,10")
  
  expect_identical(paste0(names(kfold_list[[1]]$test@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(kfold_list[[1]]$test@env$colfactors$V8, collapse=","),"6,8")
  
  expect_identical(paste0(names(kfold_list[[2]]$train@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(kfold_list[[2]]$train@env$colfactors$V8, collapse=","),"6,8")
  
  expect_identical(paste0(names(kfold_list[[2]]$test@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(kfold_list[[2]]$test@env$colfactors$V8, collapse=","),"8,10")
})

test_that("KFold works on SharkDataFrame", {
  kfold_list <- adatao.cv.kfold(data=df2,nFolds=2,seed=17)
  expect_equal(length(kfold_list),2)
  expect_equal(length(kfold_list[[1]]),2)
  expect_equal(length(kfold_list[[2]]),2)
})

test_that("KFold works on SharkDataFrame with factor columns", {
  # regression test
  df22 <- adatao.as.factor(df2, "vs")
  kfold_list <- adatao.cv.kfold(data=df22,nFolds=2,seed=17)
  expect_identical(paste0(names(kfold_list[[1]]$train@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(kfold_list[[1]]$train@env$colfactors$vs, collapse=","),"8,10")
  
  expect_identical(paste0(names(kfold_list[[1]]$test@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(kfold_list[[1]]$test@env$colfactors$vs, collapse=","),"6,8")
  
  expect_identical(paste0(names(kfold_list[[2]]$train@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(kfold_list[[2]]$train@env$colfactors$vs, collapse=","),"6,8")
  
  expect_identical(paste0(names(kfold_list[[2]]$test@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(kfold_list[[2]]$test@env$colfactors$vs, collapse=","),"8,10")
})


test_that("Random subsampling works on normal DataFrame", {
  rs_list <- adatao.cv.rs(data=df1,numrs=2,trainingSize=0.8,seed=17)
  expect_equal(length(rs_list),2)
  expect_equal(length(rs_list[[1]]),2)
  expect_equal(length(rs_list[[2]]),2)
})

test_that("Random subsampling works on normal DataFrame with factor columns", {
  # regression test
  df12 <- adatao.as.factor(df1, "V8")
  rs_list <- adatao.cv.rs(data=df12,numrs=2,trainingSize=0.8,seed=17)
  expect_identical(paste0(names(rs_list[[1]]$train@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(rs_list[[1]]$train@env$colfactors$V8, collapse=","),"10,15")
  
  expect_identical(paste0(names(rs_list[[1]]$test@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(rs_list[[1]]$test@env$colfactors$V8, collapse=","),"4,3")
  
  expect_identical(paste0(names(rs_list[[2]]$train@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(rs_list[[2]]$train@env$colfactors$V8, collapse=","),"11,14")
  
  expect_identical(paste0(names(rs_list[[2]]$test@env$colfactors$V8), collapse=","),"1.0,0.0")
  expect_identical(paste0(rs_list[[2]]$test@env$colfactors$V8, collapse=","),"3,4")
})

test_that("Random subsampling works on SharkDataFrame", {
  rs_list <- adatao.cv.rs(data=df2,numrs=2,trainingSize=0.8,seed=17)
  expect_equal(length(rs_list),2)
  expect_equal(length(rs_list[[1]]),2)
  expect_equal(length(rs_list[[2]]),2)
})

test_that("Random subsampling works on  SharkDataFrame with factor columns", {
  # regression test
  df22 <- adatao.as.factor(df2, "vs")
  rs_list <- adatao.cv.rs(data=df22,numrs=2,trainingSize=0.8,seed=17)
  expect_identical(paste0(names(rs_list[[1]]$train@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(rs_list[[1]]$train@env$colfactors$vs, collapse=","),"10,15")
  
  expect_identical(paste0(names(rs_list[[1]]$test@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(rs_list[[1]]$test@env$colfactors$vs, collapse=","),"4,3")
  
  expect_identical(paste0(names(rs_list[[2]]$train@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(rs_list[[2]]$train@env$colfactors$vs, collapse=","),"11,14")
  
  expect_identical(paste0(names(rs_list[[2]]$test@env$colfactors$vs), collapse=","),"1,0")
  expect_identical(paste0(rs_list[[2]]$test@env$colfactors$vs, collapse=","),"3,4")
})

test_that("R2 works on SharkDataFrame", {
    lm.gd <- adatao.lm.gd(mpg ~ hp + wt, data=df2, learningRate=0.00005, numIterations=10, regularized="ridge", lambda=1, initialWeights=c(37.3, -0.04, -4))
    r2 <- adatao.r2(lm.gd, df2)
    expect_equal(paste0(r2), "0.826449070999054")
  }
)          

test_that("adatao.cv.lm.gd works", {
  r2s <- adatao.cv.lm.gd(mpg ~ hp + wt, data=df2, learningRate=0.00005, numIterations=10, regularized="ridge", lambda=1, initialWeights=c(37.3, -0.04, -4),k=3,seed=17)
  expect_identical(paste0(r2s,collapse=","), "0.77157792757603,0.882319321189795,0.61742992779534")
})

test_that("adatao.cv.lm works", {
  r2s <- adatao.cv.lm(mpg ~ hp + wt, data=df2, k=2,seed=17)
  expect_identical(paste0(format(r2s),collapse=","), "0.8307514,0.6757989")
})

test_that("adatao.cv.lm works on admission", {
  r2s <- adatao.cv.lm(v1 ~ v3, data=df3, k=2,seed=17)
  #cat(paste0(format(r2s),collapse=","))
  expect_identical(paste0(format(r2s),collapse=","), "0.02472215,0.02956555")
})

test_that("adatao.cv.glm.gd works", {
  metrics <- adatao.cv.glm.gd(v1 ~ v3, data=df3, learningRate=0.1, numIterations=50, initialWeights=c(-4.6,1.5), alpha_length=100,k=2,seed=17)
  expect_true(length(metrics[[1]]$threshold)>0)
  # the glm.gd returns different weights for each running!!!!, so we cannot assert on exact values
  #expect_identical(format(metrics[[1]]$auc), "0.3804639")
})

test_that("adatao.cv.glm works", {
  metrics <- adatao.cv.glm(v1 ~ v3, data=df3, alpha_length=100,k=3,seed=17)
  #cat(format(metrics[[1]]$auc))
  expect_identical(format(metrics[[1]]$auc), "0.6221591")
})

adatao.disconnect()