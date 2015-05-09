#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
context("adatao.join")

test_that("Test for adatao.join ", {
  
adatao.connect("qa.adatao.com", username="qa1", password = "letmetest1@") # QA cluster  
  
adatao.sql('drop table if exists DaysInHospital_Y2')
adatao.sql("create external table DaysInHospital_Y2 (MemberID int, ClaimsTruncated int, DaysInHospital int
) ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
           WITH serdeproperties ( 
           'separatorChar' = ',', 
           'quoteChar' = '\"' 
           )
           STORED AS TEXTFILE LOCATION '/DaysInHospital_Y2/'");

DaysInHospital_Y2_ddf <- adatao.sql2ddf("select * from DaysInHospital_Y2")
nrow(DaysInHospital_Y2_ddf)
summary(DaysInHospital_Y2_ddf)

expect_equal(nrow(DaysInHospital_Y2_ddf), 76038)
expect_equal(ncol(DaysInHospital_Y2_ddf), 3)
             
 # Fetch ddf into a local dataframe
DaysInHospital_Y2_df <- fetchRows(DaysInHospital_Y2_ddf, nrow(DaysInHospital_Y2_ddf))
             
# test columnames, names, head
expect_identical(colnames(DaysInHospital_Y2_ddf), colnames(DaysInHospital_Y2_df))
expect_identical(names(DaysInHospital_Y2_ddf), names(DaysInHospital_Y2_df))
expect_identical( head(DaysInHospital_Y2_ddf, 1000),  head(DaysInHospital_Y2_df, 1000))
             


adatao.sql('drop table if exists Members')
adatao.sql("create external table Members (MemberID int, AgeAtFirstClaim string, Sex string
) ROW FORMAT SERDE 'com.bizo.hive.serde.csv.CSVSerde' 
           WITH serdeproperties ( 
           'separatorChar' = ',', 
           'quoteChar' = '\"' 
           )
           STORED AS TEXTFILE LOCATION '/Members/'");


Members_ddf <- adatao.sql2ddf("select * from Members") 
expect_equal(nrow(Members_ddf), 113000)
expect_equal(ncol(Members_ddf), 3)

# Fetch ddf into a local dataframe
Members_df <- fetchRows(Members_ddf, nrow(Members_ddf))

# test columnames, names, head
expect_identical(colnames(Members_ddf), colnames(Members_df))
expect_identical(names(Members_ddf), names(Members_df))
expect_identical( head(Members_ddf, 1000),  head(Members_df, 1000))


# Test inner join
DaysInHospital_Y2_inner.join_df <- merge(Members_df, DaysInHospital_Y2_df, by = 'memberid')
DaysInHospital_Y2_inner.join_ddf <- adatao.join(Members_ddf, DaysInHospital_Y2_ddf, by = 'memberid', type=c("inner"))
DaysInHospital_Y2_inner.join_ddf <- adatao.sort(DaysInHospital_Y2_inner.join_ddf, col='memberid', descending=FALSE)
expect_equivalent(DaysInHospital_Y2_inner.join_ddf,  DaysInHospital_Y2_inner.join_df)


# Test left join
DaysInHospital_Y2_left.join_df <- merge(Members_df, DaysInHospital_Y2_df, by = 'memberid', all.x = TRUE)
DaysInHospital_Y2_left.join_ddf <- adatao.join(Members_ddf, DaysInHospital_Y2_ddf, by = 'memberid', type=c("left"))
DaysInHospital_Y2_left.join_ddf <- adatao.sort(DaysInHospital_Y2_left.join_ddf, col='memberid', descending=FALSE)
expect_equivalent(DaysInHospital_Y2_left.join_ddf,  DaysInHospital_Y2_left.join_df)


# Test right join
DaysInHospital_Y2_right.join_df <- merge(Members_df, DaysInHospital_Y2_df, by = 'memberid', all.y = TRUE)
DaysInHospital_Y2_right.join_ddf <- adatao.join(Members_ddf, DaysInHospital_Y2_ddf, by = 'memberid', type=c("right"))
DaysInHospital_Y2_right.join_ddf <- adatao.sort(DaysInHospital_Y2_right.join_ddf, col='memberid', descending=FALSE)
expect_equivalent(DaysInHospital_Y2_right.join_ddf,  DaysInHospital_Y2_right.join_df)


DaysInHospital_Y2_outer.join_df <- merge(Members_df, DaysInHospital_Y2_df, by = 'memberid', all = TRUE)
DaysInHospital_Y2_full.join_ddf <- adatao.join(Members_ddf, DaysInHospital_Y2_ddf, by = 'memberid', type=c("full"))
DaysInHospital_Y2_full.join_ddf <- adatao.sort(DaysInHospital_Y2_full.join_ddf, col='memberid', descending=FALSE)
expect_equivalent(DaysInHospital_Y2_full.join_ddf,  DaysInHospital_Y2_outer.join_df)






adatao.disconnect()
})


