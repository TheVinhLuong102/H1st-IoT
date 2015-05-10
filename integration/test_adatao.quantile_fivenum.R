#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("adatao.quantile, adatao.fivenum")

cluster_ip <- "qa.adatao.com"
username <- "qa1"
password = "letmetest1@"

test_that("Test for  adatao.quantile, adatao.fivenum ", {
  
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

GiveCredit_ddf <- adatao.sql2ddf("select * from GiveCredit")
expect_equal(nrow(GiveCredit_ddf), 150000)
# Fetch to a local data frame
GiveCredit_df <- fetchRows(GiveCredit_ddf, nrow(GiveCredit_ddf))

# Test adatao.quantile
expect_equivalent(adatao.quantile(GiveCredit_ddf, "age", probs = seq(0, 1, 0.1)), 
  quantile(GiveCredit_df$age, probs = seq(0, 1, 0.1)) )

expect_equivalent(adatao.quantile(GiveCredit_ddf, "numberoftime3059dayspastduenotworse", probs = seq(0, 1, 0.1)), 
  quantile(GiveCredit_df$numberoftime3059dayspastduenotworse, probs = seq(0, 1, 0.1), na.rm=TRUE) )

expect_equivalent(adatao.quantile(GiveCredit_ddf, "monthlyincome", probs = seq(0, 1, 0.1)), 
  quantile(GiveCredit_df$monthlyincome, probs = seq(0, 1, 0.1), na.rm=TRUE) )

expect_equivalent(adatao.quantile(GiveCredit_ddf, "numberofdependents", probs = seq(0, 1, 0.1)), 
  quantile(GiveCredit_df$numberofdependents, probs = seq(0, 1, 0.1), na.rm=TRUE) )

# Test adatao.fivenum
expect_equivalent(adatao.fivenum(GiveCredit_ddf[,"numberofopencreditlinesandloans"]),
                  data.frame(t(fivenum(GiveCredit_df[,"numberofopencreditlinesandloans"], na.rm=TRUE))) )

expect_equivalent(adatao.fivenum(GiveCredit_ddf[,"numberofdependents"]),
                  data.frame(t(fivenum(GiveCredit_df[,"numberofdependents"], na.rm=TRUE))) )

expect_equivalent(adatao.fivenum(GiveCredit_ddf[,"monthlyincome"]),
                  data.frame(t(fivenum(GiveCredit_df[,"monthlyincome"], na.rm=TRUE))) )

expect_equivalent(adatao.fivenum(GiveCredit_ddf[,"age"]),
                  data.frame(t(fivenum(GiveCredit_df[,"age"], na.rm=TRUE))) )

adatao.disconnect()
})
