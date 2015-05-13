#######################################################
# (c) Copyright 2013, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("Naive Bayes")

test_that("Naive Bayes classification with confusion matrix works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/airline-transform.3.csv",sep=",")
  nb <- adatao.naiveBayes(V13 ~ V3 + V4 + V5 + V6 + V7 + V8 + V10 + V11 + V12 + V14 + V17, data=df)
  cf <- adatao.binary.confusion.matrix(model=nb,data=df)
  print(cf)
  adatao.disconnect()

  expect_equal(nb$nClasses, 2)
  expect_equal(nb$nFeatures, 11)
})