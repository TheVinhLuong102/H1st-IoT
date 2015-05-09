#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("min, mean, max, sd, var, cov, cor, scale, xtabs")
#adatao.connect("54.158.85.101", 16000, "ashish", "123") # Tom cluster
#adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster  
adatao.connect(HOST_NAME, username="testuser", password = "adata0!")

# Create churntrain ddf
adatao.sql('drop table if exists churnTrain')
adatao.sql("create external table churntrain (state string,account_length int,area_code string,international_plan string,voice_mail_plan string,number_vmail_messages int,total_day_minutes double,total_day_calls int,total_day_charge double, total_eve_minutes double,total_eve_calls double,total_eve_charge double,total_night_minutes double,total_night_calls double,total_night_charge double,total_intl_minutes double,total_intl_calls double,total_intl_charge double,number_customer_service_calls double,churn string
) ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
WITH serdeproperties ( 
  'separatorChar' = ',', 
  'quoteChar' = '\"' 
)
STORED AS TEXTFILE LOCATION '/churnTrain/'");



test_that("Test for min, mean, max, sd, var, cov, cor ", {
  
  
  churnTrain_ddf <- adatao.sql2ddf("select * from churnTrain")
  expect_equal(nrow(churnTrain_ddf), 3333)
  expect_equal(ncol(churnTrain_ddf), 20)
  
  # Fetch ddf into a local dataframe
  churnTrain_df <- fetchRows(churnTrain_ddf, nrow(churnTrain_ddf))
  
  # test columnames, names, head
  expect_identical(colnames(churnTrain_ddf), colnames(churnTrain_df))
  expect_identical(names(churnTrain_ddf), names(churnTrain_df))
  expect_identical( head(churnTrain_ddf, 1000),  head(churnTrain_df, 1000))
  
 
  
  # test min, mean, max, sd, var
  expect_equal(adatao.min(churnTrain_ddf, "total_day_minutes"), min(churnTrain_df$total_day_minutes))
  expect_equal(adatao.mean(churnTrain_ddf, "total_day_minutes"), mean(churnTrain_df$total_day_minutes))
  expect_equal(adatao.max(churnTrain_ddf, "total_day_minutes"), max(churnTrain_df$total_day_minutes))
  expect_equal(adatao.sd(churnTrain_ddf, "total_day_minutes"), sd(churnTrain_df$total_day_minutes))
  expect_equal(adatao.var(churnTrain_ddf, "total_day_minutes"), var(churnTrain_df$total_day_minutes))
   
  expect_equal(adatao.min(churnTrain_ddf, "total_intl_minutes"), min(churnTrain_df$total_intl_minutes))
  expect_equal(adatao.mean(churnTrain_ddf, "total_intl_minutes"), mean(churnTrain_df$total_intl_minutes))
  expect_equal(adatao.max(churnTrain_ddf, "total_intl_minutes"), max(churnTrain_df$total_intl_minutes))
  expect_equal(adatao.sd(churnTrain_ddf, "total_intl_minutes"), sd(churnTrain_df$total_intl_minutes))
  expect_equal(adatao.var(churnTrain_ddf, "total_intl_minutes"), var(churnTrain_df$total_intl_minutes))
  
  expect_equal(adatao.mean(churnTrain_ddf, "total_intl_calls"), mean(churnTrain_df$total_intl_calls))
  expect_equal(adatao.min(churnTrain_ddf, "total_intl_calls"), min(churnTrain_df$total_intl_calls))
  expect_equal(adatao.max(churnTrain_ddf, "total_intl_calls"), max(churnTrain_df$total_intl_calls))
  expect_equal(adatao.sd(churnTrain_ddf, "total_intl_calls"), sd(churnTrain_df$total_intl_calls))
  expect_equal(adatao.var(churnTrain_ddf, "total_intl_calls"), var(churnTrain_df$total_intl_calls))
  
  
  # Covariance Test
  expect_equal(adatao.cov(churnTrain_ddf, "total_day_minutes", "total_day_minutes"), cov(churnTrain_df$total_day_minutes, churnTrain_df$total_day_minutes))  
  expect_equal(adatao.cov(churnTrain_ddf, "total_day_minutes", "total_intl_calls"), cov(churnTrain_df$total_day_minutes, churnTrain_df$total_intl_calls))  
  expect_equal(adatao.cov(churnTrain_ddf, "total_intl_minutes", "total_day_minutes"), cov(churnTrain_df$total_intl_minutes, churnTrain_df$total_day_minutes))  
  expect_equal(adatao.cov(churnTrain_ddf, "total_intl_minutes", "total_intl_calls"), cov(churnTrain_df$total_intl_minutes,  churnTrain_df$total_intl_calls))  

  # Correlation Test
  expect_equal(adatao.cor(churnTrain_ddf, "total_day_minutes", "total_day_minutes"), cor(churnTrain_df$total_day_minutes, churnTrain_df$total_day_minutes))  
  expect_equal(adatao.cor(churnTrain_ddf, "total_day_minutes", "total_intl_calls"), cor(churnTrain_df$total_day_minutes, churnTrain_df$total_intl_calls))  
  expect_equal(adatao.cor(churnTrain_ddf, "total_intl_minutes", "total_day_minutes"), cor(churnTrain_df$total_intl_minutes, churnTrain_df$total_day_minutes))  
  expect_equal(adatao.cor(churnTrain_ddf, "total_intl_minutes", "total_intl_calls"), cor(churnTrain_df$total_intl_minutes,  churnTrain_df$total_intl_calls))  
  

})



test_that("Test for adatao.scale ", {
  
# adatao.scale Rescale and Normalization Test
R_rescale_result <-t( t(  t(t(churnTrain_df[,c(6:19)]) - apply(churnTrain_df[,c(6:19)], 2, min) ) ) / (  apply(churnTrain_df[,c(6:19)], 2, max) - apply(churnTrain_df[,c(6:19)], 2, min)  ))
adatao_rescale_result <- adatao.scale(churnTrain_ddf[,c(6:19)], type="rescaling")
expect_equivalent(fetchRows(adatao_rescale_result, nrow(adatao_rescale_result)), data.frame(R_rescale_result))

R_normalization_result <- data.frame(scale(churnTrain_df[,c(6:19)], center = TRUE, scale = TRUE))
adatao_normalization_result <- adatao.scale(churnTrain_ddf[,c(6:19)], type="normalization")
expect_equivalent(fetchRows(adatao_normalization_result, nrow(adatao_normalization_result)), R_normalization_result)

})


test_that("Test for adatao.xtabs ", {
  
expect_equivalent(adatao.xtabs(~ churn, churnTrain_ddf), xtabs(~ churn, churnTrain_df))
expect_equivalent(adatao.xtabs(~ state, churnTrain_ddf), xtabs(~ state, churnTrain_df))
expect_equivalent(adatao.xtabs(~ state + churn, churnTrain_ddf), xtabs(~ state + churn, churnTrain_df))
expect_equivalent(adatao.xtabs(~ state + area_code + churn, churnTrain_ddf), xtabs(~ state + area_code + churn, churnTrain_df))
expect_equivalent(adatao.xtabs(~ state + area_code + international_plan + churn, churnTrain_ddf), xtabs(~ state + area_code + international_plan + churn, churnTrain_df))


})


adatao.disconnect()



