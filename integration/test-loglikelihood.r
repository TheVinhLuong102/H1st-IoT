#######################################################
# (c) Copyright 2013, Adatao, Inc. All Rights Reserved.

library(adatao)
context("Log Likelihood")

test_that("Log Likelihood - Normal Equation Linear Regression works", {
  adatao.connect("localhost", 7911)
  df<-adatao.loadTable("resources/mtcars",sep=" ")
  result <- adatao.lm(V1 ~ V6, data=df)
  l <- logLik(result)
  adatao.disconnect()
  
  expect_equal(attr(l, "nall"), 32)
  expect_equal(attr(l, "nobs"), 32)
  expect_equal(attr(l, "df"), 3)
  expect_true(abs(c(l) - -80.01471) < 1e5)
  expect_true(abs(AIC(result) - 164.0294) < 1e3)
})