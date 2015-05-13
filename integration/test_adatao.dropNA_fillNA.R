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




adatao.cut does not preserve columns. It changes the coltypes of original ddf (churnTrain_ddf ) into character and does not even create the intervals in the new ddf (i.e. churnTrainCut_ddf) . Actually it should create factor columns in the new ddf (i.e. churnTrainCut_ddf) also.


The expected result was as follows:-
1. A new ddf with the column factored as specified
2. The original ddf is not affected

The observed result is as follows:-
1. A new ddf is created. However, the column is not factored as specified
2. The original ddf is not affected

adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster
adatao.sql('drop table if exists churnTrain')
adatao.sql("create external table churntrain (state string,account_length int,area_code string,international_plan string,voice_mail_plan string,number_vmail_messages int,total_day_minutes double,total_day_calls int,total_day_charge double, total_eve_minutes double,total_eve_calls double,total_eve_charge double,total_night_minutes double,total_night_calls double,total_night_charge double,total_intl_minutes double,total_intl_calls double,total_intl_charge double,number_customer_service_calls double,churn string
) ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
           WITH serdeproperties ( 
           'separatorChar' = ',', 
           'quoteChar' = '\"' 
           )
           STORED AS TEXTFILE LOCATION '/churnTrain/'");
churnTrain_ddf <- adatao.sql2ddf("select * from churnTrain")
coltypes(churnTrain_ddf[,7])
$total_day_minutes
[1] "double"

churnTrainCut_ddf <- adatao.cut(churnTrain_ddf, "total_day_minutes", breakType = "equalInterval", breaks=10)
coltypes(churnTrain_ddf[,7])
$total_day_minutes
[1] "double"

coltypes(churnTrainCut_ddf[,7])
$total_day_minutes
[1] "double"


head(churnTrain_ddf[,7])
total_day_minutes
1              265.1
2              161.6
3              243.4
4              299.4
5              166.7
6              223.4
7              218.2
8              157.0
9              184.5
10             258.6

head(churnTrainCut_ddf[,7])
total_day_minutes
1              265.1
2              161.6
3              243.4
4              299.4
5              166.7
6              223.4
7              218.2
8              157.0
9              184.5
10             258.6
