
#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)

context("adatao.cut adatao.as.numeric, adatao.as.integer, adatao.as.double, adatao.as.character, adatao.as.logical")

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
expect_identical(nrow(churnTrain_ddf), 3333)
coltypes(churnTrain_ddf[,"total_day_minutes"])


# Standard R 
churnTrain_df <- fetchRows(churnTrain_ddf, nrow(churnTrain_ddf))
expect_identical(colnames(churnTrain_ddf), colnames(churnTrain_df))


test_that("Test for  adatoa.cut ", {
  
churnTrainCut_total_day_minutes_df <- cut(churnTrain_df$total_day_minutes, breaks = 10)
# adatao.cut
churnTrainCut_ddf <- adatao.cut(churnTrain_ddf, "total_day_minutes", breakType = "equalInterval", breaks=10)
churnTrainCut_total_day_minutes_ddf <- fetchRows(churnTrainCut_ddf[,"total_day_minutes"], nrow(churnTrainCut_ddf[,"total_day_minutes"]))
expect_equivalent(churnTrainCut_total_day_minutes_ddf,  churnTrainCut_total_day_minutes_df)
expect_equivalent(coltypes(churnTrain_ddf[,"total_day_minutes"]), as.list("factor"))
})




test_that("Test for  adatoa.as.factor ", {
# adatao.factor
churnTrainFactor_ddf <- adatao.as.factor(data = churnTrain_ddf, cols = c("state", "area_code", "international_plan", "voice_mail_plan", "churn"))
expect_equivalent(coltypes(churnTrainFactor_ddf[,c("state", "area_code", "international_plan", "voice_mail_plan", "churn")]),
                  list("factor", "factor", "factor", "factor", "factor"))

expect_equivalent(sort(churnTrainFactor_ddf_summary[[2]]$state), sort(summary(as.factor(churnTrain_df[,c("state")]))) )
expect_equivalent(sort(churnTrainFactor_ddf_summary[[2]]$area_code), sort(summary(as.factor(churnTrain_df[,c("area_code")]))) )
expect_equivalent(sort(churnTrainFactor_ddf_summary[[2]]$international_plan), sort(summary(as.factor(churnTrain_df[,c("international_plan")]))) )
expect_equivalent(sort(churnTrainFactor_ddf_summary[[2]]$voice_mail_plan), sort(summary(as.factor(churnTrain_df[,c("voice_mail_plan")]))) )
expect_equivalent(sort(churnTrainFactor_ddf_summary[[2]]$churn), sort(summary(as.factor(churnTrain_df[,c("churn")]))) )
})




test_that("Test for  adatoa.as.character ", {
# adatao.as.character
churnTrainCharacter_ddf <- adatao.as.character(data = churnTrain_ddf, col = c("total_day_minutes"))
expect_equivalent(coltypes(churnTrainCharacter_ddf[,c("total_day_minutes")]), list("character"))
churnTrainCharacter_ddf_summary <- summary(churnTrainCharacter_ddf[,c("total_day_minutes")])
expect_equivalent( churnTrainCharacter_ddf_summary[[2]], list(summary(as.character(churnTrain_df[,c("total_day_minutes")]))) )
})

test_that("Test for  adatoa.as.numeric ", {
# adatao.as.numeric
churnTrainNumeric_ddf <- adatao.as.numeric(data = churnTrain_ddf, col = c("total_day_minutes"))
expect_equivalent(coltypes(churnTrainNumeric_ddf[,c("total_day_minutes")]), list("double"))
churnTrainNumeric_ddf_summary <- summary(churnTrainNumeric_ddf[,c("total_day_minutes")])
expect_equivalent( churnTrainNumeric_ddf_summary[[2]], list(summary(as.numeric(churnTrain_df[,c("total_day_minutes")]))) )
# Test Min in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[1], summary(as.numeric(churnTrain_df[,c("total_day_minutes")]))[1] ) 
# Test Max in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[2], summary(as.numeric(churnTrain_df[,c("total_day_minutes")]))[6] )
# Test Mean in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[3], summary(as.numeric(churnTrain_df[,c("total_day_minutes")]))[4] )
# Test stdev in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[4], sd(as.numeric(churnTrain_df[,c("total_day_minutes")]) ) )
# Test sum in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[5], sum(as.numeric(churnTrain_df[,c("total_day_minutes")])) )
# Test count in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[6], length(as.numeric(churnTrain_df[,c("total_day_minutes")]) ) )
# Test countNA in summary is equal
expect_equivalent(churnTrainNumeric_ddf_summary[[1]]$total_day_minutes[7], length(which(is.na(as.numeric(churnTrain_df[,c("total_day_minutes")])) == TRUE))  )
})

test_that("Test for  adatoa.as.integer ", {
# adatao.as.integer
churnTraininteger_ddf <- adatao.as.integer(data = adatao.as.character(data = churnTrain_ddf, col = c("total_day_minutes")), col = c("total_day_minutes"))
expect_equivalent(coltypes(churnTraininteger_ddf[,c("total_day_minutes")]), list("integer"))
churnTraininteger_ddf_summary <- summary(churnTraininteger_ddf[,c("total_day_minutes")])
expect_equivalent( churnTraininteger_ddf_summary[[2]], list(summary(as.integer(churnTrain_df[,c("total_day_minutes")]))) )
# Test Min in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[1], summary(as.integer(churnTrain_df[,c("total_day_minutes")]))[1] ) 
# Test Max in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[2], summary(as.integer(churnTrain_df[,c("total_day_minutes")]))[6] )
# Test Mean in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[3], summary(as.integer(churnTrain_df[,c("total_day_minutes")]))[4] )
# Test stdev in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[4], sd(as.integer(churnTrain_df[,c("total_day_minutes")]) ) )
# Test sum in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[5], sum(as.integer(churnTrain_df[,c("total_day_minutes")])) )
# Test count in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[6], length(as.integer(churnTrain_df[,c("total_day_minutes")]) ) )
# Test countNA in summary is equal
expect_equivalent(churnTraininteger_ddf_summary[[1]]$total_day_minutes[7], length(which(is.na(as.integer(churnTrain_df[,c("total_day_minutes")])) == TRUE))  )
})



test_that("Test for  adatoa.as.double ", {
# adatao.as.double
churnTraindouble_ddf <- adatao.as.double(data = adatao.as.character(data = churnTrain_ddf, col = c("total_day_minutes")), col = c("total_day_minutes"))
expect_equivalent(coltypes(churnTraindouble_ddf[,c("total_day_minutes")]), list("double"))
churnTraindouble_ddf_summary <- summary(churnTraindouble_ddf[,c("total_day_minutes")])
expect_equivalent( churnTraindouble_ddf_summary[[2]], list(summary(as.double(churnTrain_df[,c("total_day_minutes")]))) )
# Test Min in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[1], summary(as.double(churnTrain_df[,c("total_day_minutes")]))[1] ) 
# Test Max in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[2], summary(as.double(churnTrain_df[,c("total_day_minutes")]))[6] )
# Test Mean in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[3], summary(as.double(churnTrain_df[,c("total_day_minutes")]))[4] )
# Test stdev in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[4], sd(as.double(churnTrain_df[,c("total_day_minutes")]) ) )
# Test sum in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[5], sum(as.double(churnTrain_df[,c("total_day_minutes")])) )
# Test count in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[6], length(as.double(churnTrain_df[,c("total_day_minutes")]) ) )
# Test countNA in summary is equal
expect_equivalent(churnTraindouble_ddf_summary[[1]]$total_day_minutes[7], length(which(is.na(as.double(churnTrain_df[,c("total_day_minutes")])) == TRUE))  )

})


test_that("Test for  adatoa.as.logical ", {
# adatao.as.logical
churnTrainTransform_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "churn_logical = if(churn == \"yes\", TRUE,FALSE)" )
churnTrainLogical_ddf <- adatao.as.logical(data = churnTrainTransform_ddf, col = c("churn_logical"))
churnTrainLogical_ddf_summary <- summary(churnTrainLogical_ddf[,c("churn_logical")])
expect_equivalent( churnTrainLogical_ddf_summary[[2]], list(summary(as.logical(churnTrain_df[,c("churn_logical")]))) )
churnTrain_df <- transform(churnTrain_df, churn_logical = ifelse( churn == "yes", TRUE, FALSE) )
# Test Min in summary is equal
expect_equivalent(churnTrainLogical_ddf_summary[[1]]$churn_logical[1], summary(churnTrain_df$churn_logical)[1] ) 
# Test Max in summary is equal
expect_equivalent(churnTrainLogical_ddf_summary[[1]]$churn_logical[2], summary(churnTrain_df$churn_logical)[2] )
# Test Mean in summary is equal
expect_equivalent(churnTrainLogical_ddf_summary[[1]]$churn_logical[3], summary(churnTrain_df$churn_logical)[3] )
# Test stdev in summary is equal
expect_equivalent(churnTrainLogical_ddf_summary[[1]]$churn_logical[4], summary(churnTrain_df$churn_logical)[4] )

})


adatao.disconnect()