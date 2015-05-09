
#####################################################
# (c) Copyright 2015, Adatao, Inc. All Rights Reserved.

library(adatao)
library(testthat)
library(stringr)

context("adatao.transform calculated fields")

test_that("Test for  adatoa.transform calculated fields ", {

        adatao.connect("54.159.221.179", username="testuser", password = "adata0!") # Huan cluster
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
        nrow(churnTrain_ddf)
        summary(churnTrain_ddf)
        
        # Standard R 
        churnTrain_df <- fetchRows(churnTrain_ddf, nrow(churnTrain_ddf))

        # test columnames, names, head
        expect_identical(colnames(churnTrain_ddf), colnames(churnTrain_df))
        expect_identical(names(churnTrain_ddf), names(churnTrain_df))
        expect_identical( head(churnTrain_ddf, 1000),  head(churnTrain_df, 1000))
        
        
        summary(churnTrain_ddf)
        
        # Create factors 
        
        churnTrain_ddf <- adatao.transform(churnTrain_ddf, churn_binary = ifelse(churn == "yes", 1,0))
        coltypes(churnTrain_ddf)
        
        adatao.as.factor(data = churnTrain_ddf, cols = c("state", "area_code", "international_plan", "voice_mail_plan", "churn"))
        coltypes(churnTrain_ddf)
        summary(churnTrain_ddf)
        
        
        
        
        # Test binary conversion
        churnTrain_df$churn_binary <- ifelse(churnTrain_df$churn == "yes", 1, 0)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "churn_binary = if(churn == \"yes\", 1,0)")
        churn_binary_Hive <- fetchRows(churnTrain_transformHive_ddf[,"churn_binary"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(churn_binary_Hive$churn_binary,  churnTrain_df$churn_binary)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"churn_binary"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", churn_binary = ifelse(churn == "yes", 1,0))
        churn_binary_R <- fetchRows(churnTrain_transformR_ddf[,"churn_binary"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(churn_binary_R$churn_binary,  churnTrain_df$churn_binary)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"churn_binary"]), as.list("integer"))
        
        # Test logical conversion
        churnTrain_df$churn_logical <- ifelse(churnTrain_df$churn == "yes", TRUE, FALSE)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "churn_logical = if(churn == \"yes\", TRUE,FALSE)")
        churn_logical_Hive <- fetchRows(churnTrain_transformHive_ddf[,"churn_logical"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(churn_logical_Hive$churn_logical,  churnTrain_df$churn_logical)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"churn_logical"]), as.list("logical"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", churn_logical = ifelse(churn == "yes", TRUE,FALSE))
        churn_logical_R <- fetchRows(churnTrain_transformR_ddf[,"churn_logical"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(churn_logical_R$churn_logical,  churnTrain_df$churn_logical)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"churn_logical"]), as.list("logical"))
        
        
        
        
        # Test total_day_minutes round to zero 
        churnTrain_df$total_day_minutes_round <- round(churnTrain_df$total_day_minutes, 0)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_minutes_round = round(total_day_minutes, 0)")
        total_day_minutes_round_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_minutes_round"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_minutes_round_Hive$total_day_minutes_round,  churnTrain_df$total_day_minutes_round)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_minutes_round"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_minutes_round = round(total_day_minutes, 0))
        total_day_minutes_round_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_minutes_round"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_minutes_round_R$total_day_minutes_round,  churnTrain_df$total_day_minutes_round)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_minutes_round"]), as.list("double"))


        # Test total_day_charge round to zero 
        churnTrain_df$total_day_charge_round <- round(churnTrain_df$total_day_charge, 0)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_round = round(total_day_charge, 0)")
        total_day_charge_round_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_round"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_round_Hive$total_day_charge_round,  churnTrain_df$total_day_charge_round)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_round"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_round = round(total_day_charge, 0))
        total_day_charge_round_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_round"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_round_R$total_day_charge_round,  churnTrain_df$total_day_charge_round)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_round"]), as.list("double"))


        # Test total_day_charge round to 1
        churnTrain_df$total_day_charge_round <- round(churnTrain_df$total_day_charge, 1)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_round = round(total_day_charge, 0)")
        total_day_charge_round_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_round"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_round_Hive$total_day_charge_round,  churnTrain_df$total_day_charge_round)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_round"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_round = round(total_day_charge, 1))
        total_day_charge_round_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_round"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_round_R$total_day_charge_round,  churnTrain_df$total_day_charge_round)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_round"]), as.list("double"))

        
        # Test total_day_minutes floor 
        churnTrain_df$total_day_minutes_floor <- floor(churnTrain_df$total_day_minutes)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_minutes_floor = floor(total_day_minutes)")
        total_day_minutes_floor_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_minutes_floor"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_minutes_floor_Hive$total_day_minutes_floor,  churnTrain_df$total_day_minutes_floor)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_minutes_floor"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_minutes_floor = floor(total_day_minutes))
        total_day_minutes_floor_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_minutes_floor"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_minutes_floor_R$total_day_minutes_floor,  churnTrain_df$total_day_minutes_floor)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_minutes_floor"]), as.list("integer"))
        

        # Test total_day_charge floor 
        churnTrain_df$total_day_charge_floor <- floor(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_floor = floor(total_day_charge)")
        total_day_charge_floor_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_floor"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_floor_Hive$total_day_charge_floor,  churnTrain_df$total_day_charge_floor)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_floor"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_floor = floor(total_day_charge))
        total_day_charge_floor_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_floor"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_floor_R$total_day_charge_floor,  churnTrain_df$total_day_charge_floor)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_floor"]), as.list("integer"))

        
        # Test total_day_minutes ceiling 
        churnTrain_df$total_day_minutes_ceiling <- ceiling(churnTrain_df$total_day_minutes)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_minutes_ceiling = ceiling(total_day_minutes)")
        total_day_minutes_ceiling_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_minutes_ceiling"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_minutes_ceiling_Hive$total_day_minutes_ceiling,  churnTrain_df$total_day_minutes_ceiling)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_minutes_ceiling"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_minutes_ceiling = ceiling(total_day_minutes))
        total_day_minutes_ceiling_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_minutes_ceiling"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_minutes_ceiling_R$total_day_minutes_ceiling,  churnTrain_df$total_day_minutes_ceiling)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_minutes_ceiling"]), as.list("integer"))
        
        
        # Test total_day_charge ceiling 
        churnTrain_df$total_day_charge_ceiling <- ceiling(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_ceiling = ceiling(total_day_charge)")
        total_day_charge_ceiling_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_ceiling"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_ceiling_Hive$total_day_charge_ceiling,  churnTrain_df$total_day_charge_ceiling)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_ceiling"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_ceiling = ceiling(total_day_charge))
        total_day_charge_ceiling_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_ceiling"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_ceiling_R$total_day_charge_ceiling,  churnTrain_df$total_day_charge_ceiling)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_ceiling"]), as.list("integer"))


        # Test total_day_charge pow 
        churnTrain_df$total_day_charge_pow <- (churnTrain_df$total_day_charge)^2
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_pow = pow(total_day_charge, 2)")
        total_day_charge_pow_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_pow"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_pow_Hive$total_day_charge_pow,  churnTrain_df$total_day_charge_pow)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_pow"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_pow = (total_day_charge)^2)
        total_day_charge_pow_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_pow"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_pow_R$total_day_charge_pow,  churnTrain_df$total_day_charge_pow)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_pow"]), as.list("double"))
        
        
        churnTrain_df$total_day_charge_pow <- (churnTrain_df$total_day_charge)^5.67812
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_pow = pow(total_day_charge, 5.67812)")
        total_day_charge_pow_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_pow"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_pow_Hive$total_day_charge_pow,  churnTrain_df$total_day_charge_pow)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_pow"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_pow = (total_day_charge)^5.67812)
        total_day_charge_pow_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_pow"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_pow_R$total_day_charge_pow,  churnTrain_df$total_day_charge_pow)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_pow"]), as.list("double"))



        
        # Test total_day_charge exp 
        churnTrain_df$total_day_charge_exp <- exp(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_exp = exp(total_day_charge)")
        total_day_charge_exp_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_exp"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_exp_Hive$total_day_charge_exp,  churnTrain_df$total_day_charge_exp)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_exp"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_exp = exp(total_day_charge))
        total_day_charge_exp_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_exp"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_exp_R$total_day_charge_exp,  churnTrain_df$total_day_charge_exp)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_exp"]), as.list("double"))
        
        
        
        # Test total_day_charge ln 
        churnTrain_df$total_day_charge_ln <- log(churnTrain_df$total_day_charge, base = exp(1))
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_ln = ln(total_day_charge)")
        total_day_charge_ln_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_ln"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_ln_Hive$total_day_charge_ln,  churnTrain_df$total_day_charge_ln)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_ln"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_ln = log(total_day_charge,  base = exp(1)) )
        total_day_charge_ln_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_ln"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_ln_R$total_day_charge_ln,  churnTrain_df$total_day_charge_ln)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_ln"]), as.list("double"))
        
        
        # Test total_day_charge log2
        churnTrain_df$total_day_charge_log2 <- log2(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_log2 = log2(total_day_charge)")
        total_day_charge_log2_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_log2"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_log2_Hive$total_day_charge_log2,  churnTrain_df$total_day_charge_log2)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_log2"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_log2 = log2(total_day_charge))
        total_day_charge_log2_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_log2"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_log2_R$total_day_charge_log2,  churnTrain_df$total_day_charge_log2)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_log2"]), as.list("double"))
        
        
        
        # Test total_day_charge log
        churnTrain_df$total_day_charge_log <- log(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_log = log(total_day_charge)")
        total_day_charge_log_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_log"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_log_Hive$total_day_charge_log,  churnTrain_df$total_day_charge_log)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_log"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_log = log(total_day_charge))
        total_day_charge_log_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_log"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_log_R$total_day_charge_log,  churnTrain_df$total_day_charge_log)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_log"]), as.list("double"))
        
        
        
        # Test total_day_charge log10
        churnTrain_df$total_day_charge_log10 <- log10(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_log10 = log10(total_day_charge)")
        total_day_charge_log10_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_log10"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_log10_Hive$total_day_charge_log10,  churnTrain_df$total_day_charge_log10)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_log10"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_log10 = log10(total_day_charge))
        total_day_charge_log10_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_log10"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_log10_R$total_day_charge_log10,  churnTrain_df$total_day_charge_log10)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_log10"]), as.list("double"))
        
        
        
        # Test total_day_charge sign
        churnTrain_df$total_day_charge_sign <- sign(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_sign = sign(total_day_charge)")
        total_day_charge_sign_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_sign"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_sign_Hive$total_day_charge_sign,  churnTrain_df$total_day_charge_sign)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_sign"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_sign = sign(total_day_charge))
        total_day_charge_sign_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_sign"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_sign_R$total_day_charge_sign,  churnTrain_df$total_day_charge_sign)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_sign"]), as.list("double"))
        
        
        
        # Test total_day_charge abs
        churnTrain_df$total_day_charge_abs <- abs(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_abs = abs(total_day_charge)")
        total_day_charge_abs_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_abs"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_abs_Hive$total_day_charge_abs,  churnTrain_df$total_day_charge_abs)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_abs"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_abs = abs(total_day_charge))
        total_day_charge_abs_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_abs"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_abs_R$total_day_charge_abs,  churnTrain_df$total_day_charge_abs)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_abs"]), as.list("double"))
        
        
        
        
        # Test total_day_charge sign (negative values)
        churnTrain_df$total_day_charge_sign <- sign(-1 * churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_sign = sign(-1 * total_day_charge)")
        total_day_charge_sign_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_sign"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_sign_Hive$total_day_charge_sign,  churnTrain_df$total_day_charge_sign)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_sign"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_sign = sign(-1 * total_day_charge))
        total_day_charge_sign_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_sign"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_sign_R$total_day_charge_sign,  churnTrain_df$total_day_charge_sign)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_sign"]), as.list("double"))
        
        
        
        # Test total_day_charge abs (negative values)
        churnTrain_df$total_day_charge_abs <- abs(-1 * churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_abs = abs(-1 * total_day_charge)")
        total_day_charge_abs_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_abs"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_abs_Hive$total_day_charge_abs,  churnTrain_df$total_day_charge_abs)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_abs"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_abs = abs(-1 * total_day_charge))
        total_day_charge_abs_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_abs"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_abs_R$total_day_charge_abs,  churnTrain_df$total_day_charge_abs)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_abs"]), as.list("double"))
        
        
        # Test total_day_charge pmod
        churnTrain_df$total_day_charge_pmod <- churnTrain_df$total_day_charge %% 5
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_pmod = pmod(total_day_charge, 5)")
        total_day_charge_pmod_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_pmod"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_pmod_Hive$total_day_charge_pmod,  churnTrain_df$total_day_charge_pmod)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_pmod"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_pmod = total_day_charge %% 5)
        total_day_charge_pmod_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_pmod"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_pmod_R$total_day_charge_pmod,  churnTrain_df$total_day_charge_pmod)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_pmod"]), as.list("double"))
        
        
        
        
        
        # Test area_code lower
        churnTrain_df$area_code_lower <- tolower(churnTrain_df$area_code)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_lower = lower(area_code)")
        area_code_lower_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_lower"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_lower_Hive$area_code_lower,  churnTrain_df$area_code_lower)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_lower"]), as.list("character"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_lower = tolower(area_code))
        area_code_lower_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_lower"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_lower_R$area_code_lower,  churnTrain_df$area_code_lower)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_lower"]), as.list("character"))
        
        
        
        
        # Test area_code upper
        churnTrain_df$area_code_upper <- toupper(churnTrain_df$area_code)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_upper = upper(area_code)")
        area_code_upper_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_upper"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_upper_Hive$area_code_upper,  churnTrain_df$area_code_upper)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_upper"]), as.list("character"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_upper = toupper(area_code))
        area_code_upper_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_upper"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_upper_R$area_code_upper,  churnTrain_df$area_code_upper)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_upper"]), as.list("character"))
        
        
        
        
        # Test area_code length
        churnTrain_df$area_code_length <- nchar(churnTrain_df$area_code)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_length = length(area_code)")
        area_code_length_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_length"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_length_Hive$area_code_length,  churnTrain_df$area_code_length)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_length"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_length = nchar(area_code))
        area_code_length_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_length"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_length_R$area_code_length,  churnTrain_df$area_code_length)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_length"]), as.list("integer"))
        
        
        
        
        # Test area_code reverse
        churnTrain_df$area_code_reverse <- apply(as.matrix(churnTrain_df$area_code), 1, function(a){paste(rev(substring(a,1:nchar(a),1:nchar(a))),collapse="")})
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_reverse = reverse(area_code)")
        area_code_reverse_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_reverse"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_reverse_Hive$area_code_reverse,  churnTrain_df$area_code_reverse)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_reverse"]), as.list("character"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_reverse = apply(area_code, 1, function(a){paste(rev(substring(a,1:nchar(a),1:nchar(a))),collapse="")})  ) 
        area_code_reverse_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_reverse"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_reverse_R$area_code_reverse,  churnTrain_df$area_code_reverse)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_reverse"]), as.list("character"))
        
        
        # Test area_code substr
        churnTrain_df$area_code_substr <-substr(churnTrain_df$area_code, 1,10)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_substr = substr(area_code, 1, 10)")
        area_code_substr_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_substr"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_substr_Hive$area_code_substr,  churnTrain_df$area_code_substr)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_substr"]), as.list("character"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_substr = substr(area_code, 1, 10))
        area_code_substr_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_substr"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_substr_R$area_code_substr,  churnTrain_df$area_code_substr)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_substr"]), as.list("character"))
        
        
        
        
        # Test area_code concat_ws
        churnTrain_df$area_code_concat_ws <-paste("      " , churnTrain_df$area_code, sep =  "   , ")
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_concat_ws = concat_ws('   - ', area_code, '    ')")
        area_code_concat_ws_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_concat_ws"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_concat_ws_Hive$area_code_concat_ws,  churnTrain_df$area_code_concat_ws)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_concat_ws"]), as.list("character"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_concat_ws = paste("      " , churnTrain_df$area_code, sep =  "   , "))
        area_code_concat_ws_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_concat_ws"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_concat_ws_R$area_code_concat_ws,  churnTrain_df$area_code_concat_ws)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_concat_ws"]), as.list("character"))
        
        
        
        
        # Test area_code trim
        library(stringr)
        churnTrain_df$area_code_trim <- str_trim(churnTrain_df$area_code, side = "both")
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "area_code_trim = trim(area_code)")
        area_code_trim_Hive <- fetchRows(churnTrain_transformHive_ddf[,"area_code_trim"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(area_code_trim_Hive$area_code_trim,  churnTrain_df$area_code_trim)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"area_code_trim"]), as.list("character"))
        
        library(stringr)
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_trim = str_trim(area_code, side = "both"))
        library(gdata)
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", area_code_trim = trim(area_code))
        area_code_trim_R <- fetchRows(churnTrain_transformR_ddf[,"area_code_trim"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(area_code_trim_R$area_code_trim,  churnTrain_df$area_code_trim)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"area_code_trim"]), as.list("character"))
        
        
        
        # Test total_day_charge max 
        churnTrain_df$total_day_charge_max <- max(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_max = max(total_day_charge)")
        total_day_charge_max_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_max"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_max_Hive$total_day_charge_max,  churnTrain_df$total_day_charge_max)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_max"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_max = max(total_day_charge))
        total_day_charge_max_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_max"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_max_R$total_day_charge_max,  churnTrain_df$total_day_charge_max)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_max"]), as.list("double"))
        
        
        # Test total_day_charge min 
        churnTrain_df$total_day_charge_min <- min(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_min = min(total_day_charge)")
        total_day_charge_min_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_min"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_min_Hive$total_day_charge_min,  churnTrain_df$total_day_charge_min)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_min"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_min = min(total_day_charge))
        total_day_charge_min_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_min"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_min_R$total_day_charge_min,  churnTrain_df$total_day_charge_min)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_min"]), as.list("double"))
        
        
        
        # Test total_day_charge sum 
        churnTrain_df$total_day_charge_sum <- sum(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_sum = sum(total_day_charge)")
        total_day_charge_sum_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_sum"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_sum_Hive$total_day_charge_sum,  churnTrain_df$total_day_charge_sum)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_sum"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_sum = sum(total_day_charge))
        total_day_charge_sum_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_sum"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_sum_R$total_day_charge_sum,  churnTrain_df$total_day_charge_sum)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_sum"]), as.list("double"))
        
        
        # Test total_day_charge count 
        churnTrain_df$total_day_charge_count <- length(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_count = count(total_day_charge)")
        total_day_charge_count_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_count"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_count_Hive$total_day_charge_count,  churnTrain_df$total_day_charge_count)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_count"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_count = length(total_day_charge))
        total_day_charge_count_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_count"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_count_R$total_day_charge_count,  churnTrain_df$total_day_charge_count)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_count"]), as.list("integer"))
        
        
        
        
        # Test total_day_charge unique count 
        churnTrain_df$total_day_charge_count <- length(unique(churnTrain_df$total_day_charge))
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_count = count(distinct total_day_charge)")
        total_day_charge_count_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_count"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_count_Hive$total_day_charge_count,  churnTrain_df$total_day_charge_count)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_count"]), as.list("integer"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_count = length(unique(total_day_charge))
        total_day_charge_count_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_count"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_count_R$total_day_charge_count,  churnTrain_df$total_day_charge_count)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_count"]), as.list("integer"))
        
        
        
        
        # Test total_day_charge var_pop 
        churnTrain_df$total_day_charge_var_pop <- var(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_var_pop = var_pop(total_day_charge)")
        total_day_charge_var_pop_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_var_pop"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_var_pop_Hive$total_day_charge_var_pop,  churnTrain_df$total_day_charge_var_pop)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_var_pop"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_var_pop = var(total_day_charge))
        total_day_charge_var_pop_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_var_pop"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_var_pop_R$total_day_charge_var_pop,  churnTrain_df$total_day_charge_var_pop)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_var_pop"]), as.list("double"))
        
        
        
        
        # Test total_day_charge stdev_pop 
        churnTrain_df$total_day_charge_stdev_pop <- var(churnTrain_df$total_day_charge)
        
        churnTrain_transformHive_ddf <- adatao.transform(churnTrain_ddf, method = "Hive", "total_day_charge_stdev_pop = stdev_pop(total_day_charge)")
        total_day_charge_stdev_pop_Hive <- fetchRows(churnTrain_transformHive_ddf[,"total_day_charge_stdev_pop"], nrow(churnTrain_transformHive_ddf))
        expect_equivalent(total_day_charge_stdev_pop_Hive$total_day_charge_stdev_pop,  churnTrain_df$total_day_charge_stdev_pop)
        expect_equivalent(coltypes(churnTrain_transformHive_ddf[,"total_day_charge_stdev_pop"]), as.list("double"))
        
        churnTrain_transformR_ddf <- adatao.transform(churnTrain_ddf, method = "R", total_day_charge_stdev_pop = var(total_day_charge))
        total_day_charge_stdev_pop_R <- fetchRows(churnTrain_transformR_ddf[,"total_day_charge_stdev_pop"], nrow(churnTrain_transformR_ddf))
        expect_equivalent(total_day_charge_stdev_pop_R$total_day_charge_stdev_pop,  churnTrain_df$total_day_charge_stdev_pop)
        expect_equivalent(coltypes(churnTrain_transformR_ddf[,"total_day_charge_stdev_pop"]), as.list("double"))






       
adatao.disconnect()
})


