#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("adatao.aggregate and adatao.grouppby")

cluster_ip <- "qa.adatao.com"
username <- "qa1"
password = "letmetest1@"


  
adatao.connect(cluster_ip, username=username, password = password) # QA cluster

#adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster  
adatao.sql("drop table if exists machine")
adatao.sql("CREATE external TABLE machine (vendor_name  string, model_name string, myct int, mmin int, mmax int, cach int, chmin int,  chmax int, perf int, estperf int) 
ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
WITH serdeproperties ( 
  'separatorChar' = ',', 
  'quoteChar' = '\"' 
)
STORED AS TEXTFILE LOCATION '/machine/'");

test_that("Test for  adatoa.aggregate ", {
  
machine_ddf <- adatao.sql2ddf("select * from machine")
expect_equal(nrow(machine_ddf), 209)



adatao_vendor_mean <- adatao.aggregate(perf ~  vendor_name, data = machine_ddf, FUN=mean)
adatao_vendor_sum <- adatao.aggregate(perf ~  vendor_name, data = machine_ddf, FUN=sum)
adatao_vendor_median <- adatao.aggregate(perf ~  vendor_name, data = machine_ddf, FUN=median)
adatao_vendor_count <- adatao.aggregate(perf ~  vendor_name, data = machine_ddf, FUN=count)
adatao_vendor_variance <- adatao.aggregate(perf ~  vendor_name, data = machine_ddf, FUN=variance)

# Standard R
machine_df <- fetchRows(machine_ddf, nrow(machine_ddf))
R_vendor_mean <- aggregate(perf ~ vendor_name, data=machine_df, FUN=mean)
R_vendor_sum <- aggregate(perf ~ vendor_name, data=machine_df, FUN=sum)
R_vendor_median <- aggregate(perf ~ vendor_name, data=machine_df, FUN=median)
R_vendor_count <- aggregate(perf ~ vendor_name, data=machine_df, FUN=length)
R_vendor_variance <- aggregate(perf ~ vendor_name, data=machine_df, FUN=var)
R_vendor_stddev <- aggregate(perf ~ vendor_name, data=machine_df, FUN=sd)

# Check equivalence of results
expect_equivalent(adatao_vendor_mean[order(adatao_vendor_mean$vendor_name), ], transform(R_vendor_mean, perf = round(perf,2)) )
expect_equivalent(adatao_vendor_sum[order(adatao_vendor_sum$vendor_name), ], transform(R_vendor_sum, perf = round(perf,2)) )
expect_equivalent(adatao_vendor_median[order(adatao_vendor_median$vendor_name), ], transform(R_vendor_median, perf = round(perf,2)) )
expect_equivalent(adatao_vendor_count[order(adatao_vendor_count$vendor_name), ], transform(R_vendor_count, perf = round(perf,2)) )
expect_equivalent(adatao_vendor_variance[order(adatao_vendor_variance$vendor_name), ], transform(R_vendor_variance, perf = round(perf,2)) )

})



test_that("Test for  adatoa.groupby ", {
  
adatao_vendor_mean <- adatao.groupby(machine_ddf, agg.cols=c("avg(perf)"), by=c("vendor_name"))
adatao_vendor_mean <- fetchRows(adatao_vendor_mean, nrow(adatao_vendor_mean))

adatao_vendor_sum <- adatao.groupby(machine_ddf, agg.cols=c("sum(perf)"), by=c("vendor_name"))
adatao_vendor_sum <- fetchRows(adatao_vendor_sum, nrow(adatao_vendor_sum))

adatao_vendor_median <- adatao.groupby(machine_ddf, agg.cols=c("median(perf)"), by=c("vendor_name"))
adatao_vendor_median <- fetchRows(adatao_vendor_median, nrow(adatao_vendor_median))

adatao_vendor_count <- adatao.groupby(machine_ddf, agg.cols=c("count(perf)"), by=c("vendor_name"))
adatao_vendor_count <- fetchRows(adatao_vendor_count, nrow(adatao_vendor_count))

adatao_vendor_var <- adatao.groupby(machine_ddf, agg.cols=c("variance(perf)"), by=c("vendor_name"))
adatao_vendor_var <- fetchRows(adatao_vendor_var, nrow(adatao_vendor_var))

adatao_vendor_stddev <- adatao.groupby(machine_ddf, agg.cols=c("stddev(perf)"), by=c("vendor_name"))
adatao_vendor_stddev <- fetchRows(adatao_vendor_stddev, nrow(adatao_vendor_stddev))

expect_equivalent(adatao_vendor_mean[order(adatao_vendor_mean$vendor_name), c(2,1)], R_vendor_mean )
expect_equivalent(adatao_vendor_sum[order(adatao_vendor_sum$vendor_name), c(2,1)], R_vendor_sum )
expect_equivalent(adatao_vendor_median[order(adatao_vendor_median$vendor_name), c(2,1)], R_vendor_median )
expect_equivalent(adatao_vendor_count[order(adatao_vendor_count$vendor_name), c(2,1)], R_vendor_count )
expect_equivalent(adatao_vendor_var[order(adatao_vendor_var$vendor_name), c(2,1)], R_vendor_variance )
expect_equivalent(adatao_vendor_stddev[order(adatao_vendor_var$vendor_name), c(2,1)], R_vendor_stddev )

})


adatao.disconnect()