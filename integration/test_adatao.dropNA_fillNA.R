#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
library(timeseries)
context("adatao.quantile, adatao.fivenum")

cluster_ip <- "qa.adatao.com"
username <- "qa1"
password = "letmetest1@"

  adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster
  
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
  

test_that("Test for  adatao.dropNA ", {
  
  
  GiveCredit_ddf <- adatao.sql2ddf("select * from GiveCredit")
  expect_equal(nrow(GiveCredit_ddf), 150000)
  # Fetch to a local data frame
  GiveCredit_df <- fetchRows(GiveCredit_ddf, nrow(GiveCredit_ddf))
  # Test Drop NA
  GiveCredit_noNA_ddf <- adatao.dropNA(GiveCredit_ddf)
  GiveCredit_noNA_df <- GiveCredit_df[GiveCredit_df[!is.na(GiveCredit_df)],]
  expect_equivalent(fetchRows(GiveCredit_noNA_ddf, nrow(GiveCredit_noNA_ddf)), GiveCredit_noNA_df)
  
  GiveCredit_DropMonthlyIncomeNA_df <- GiveCredit_df[!is.na(GiveCredit_df$monthlyincome),]
  GiveCredit_DropMonthlyIncomeNA_ddf <- adatao.dropNA(GiveCredit_ddf[,"monthlyincome"], "column", "all")
  expect_equivalent(fetchRows(GiveCredit_DropMonthlyIncomeNA_ddf, nrow(GiveCredit_DropMonthlyIncomeNA_ddf)), GiveCredit_DropMonthlyIncomeNA_df$monthlyincome)
  
  GiveCredit_DropNumberOfDependentsNA_df <- GiveCredit_df[!is.na(GiveCredit_df$numberofdependents),]
  GiveCredit_DropNumberOfDependentsNA_ddf <- adatao.dropNA(GiveCredit_ddf[,"numberofdependents"], "column", "all")
  expect_equivalent(fetchRows(GiveCredit_DropNumberOfDependentsNA_ddf, nrow(GiveCredit_DropNumberOfDependentsNA_ddf)), GiveCredit_DropNumberOfDependentsNA_df$numberofdependents)
  
})


test_that("Test for  adatao.fillNA", {
  
  # Test fillNA
  library(timeSeries)
  # Impute with Mean
  giveCredit.ImputeWithMean_df <- GiveCredit_df
  giveCredit.ImputeWithMean_df$monthlyincome <- substituteNA(giveCredit.ImputeWithMean_df$monthlyincome, type="mean")
  giveCredit.ImputeWithMean_df$numberofdependents <- substituteNA(giveCredit.ImputeWithMean_df$numberofdependents, type="mean")  
  GiveCredit_FillMeanMonthlyIncomeNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"monthlyincome"], aggregation.func=mean)
  GiveCredit_FillMeanNumberOfDependentsNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"numberofdependents"], aggregation.func=mean)
  expect_equivalent(fetchRows(GiveCredit_FillMeanMonthlyIncomeNA_ddf, nrow(GiveCredit_FillMeanMonthlyIncomeNA_ddf)), giveCredit.ImputeWithMean_df$monthlyincome)
  expect_equivalent(fetchRows(GiveCredit_FillMeanNumberOfDependentsNA_ddf, nrow(GiveCredit_FillMeanNumberOfDependentsNA_ddf)), giveCredit.ImputeWithMean_df$numberofdependents)
  
  # Impute with Median
  giveCredit.ImputeWithMedian_df <- GiveCredit_df
  giveCredit.ImputeWithMedian_df$monthlyincome <- substituteNA(giveCredit.ImputeWithMedian_df$monthlyincome, type="median")
  giveCredit.ImputeWithMedian_df$numberofdependents <- substituteNA(giveCredit.ImputeWithMedian_df$numberofdependents, type="median")
  GiveCredit_FillMedianMonthlyIncomeNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"monthlyincome"], aggregation.func=median)
  GiveCredit_FillMedianNumberOfDependentsNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"numberofdependents"], aggregation.func=median)
  expect_equivalent(fetchRows(GiveCredit_FillMedianMonthlyIncomeNA_ddf, nrow(GiveCredit_FillMedianMonthlyIncomeNA_ddf)), giveCredit.ImputeWithMedian_df$monthlyincome)
  expect_equivalent(fetchRows(GiveCredit_FillMedianNumberOfDependentsNA_ddf, nrow(GiveCredit_FillMedianNumberOfDependentsNA_ddf)), giveCredit.ImputeWithMedian_df$numberofdependents)
  
  # Impute with Zero
  giveCredit.ImputeWithZero_df <- GiveCredit_df
  giveCredit.ImputeWithZero_df$monthlyincome <- substituteNA(giveCredit.ImputeWithZero_df$monthlyincome, type="zeros")
  giveCredit.ImputeWithZero_df$numberofdependents <- substituteNA(giveCredit.ImputeWithZero_df$numberofdependents, type="zeros")  
  GiveCredit_FillZeroMonthlyIncomeNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"monthlyincome"], value=0)
  GiveCredit_FillZeroNumberOfDependentsNA_ddf <- adatao.fillNA(GiveCredit_ddf[,"numberofdependents"], value=0)
  expect_equivalent(fetchRows(GiveCredit_FillZeroMonthlyIncomeNA_ddf, nrow(GiveCredit_FillZeroMonthlyIncomeNA_ddf)), giveCredit.ImputeWithZero_df$monthlyincome)
  expect_equivalent(fetchRows(GiveCredit_FillZeroNumberOfDependentsNA_ddf, nrow(GiveCredit_FillZeroNumberOfDependentsNA_ddf)), giveCredit.ImputeWithZero_df$numberofdependents)
  
})

adatao.disconnect()



