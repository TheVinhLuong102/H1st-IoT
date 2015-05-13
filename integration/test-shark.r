library(adatao)
context("Shark Tests")
adatao.connect("localhost", 7911)

adatao.sql("set shark.test.data.path=resources/sharkfiles")
adatao.sql("drop table if exists test")
adatao.sql("CREATE TABLE test (key INT, val STRING)")
adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/kv1.txt' INTO TABLE test")

test_that("SQL to ADATAO DataFrame works", {
  ret <- adatao.sql("describe test")
  expect_identical(paste(ret,collapse=","), "key\tint\t,val\tstring\t")
  ret <- adatao.sql2ddf("SELECT * FROM test LIMIT 1")
  rows <- fetchRows(ret,1)
  expect_identical(paste0(rows,collapse=","), "238,val_238")
})

test_that("SQL to small data works", {
  rows <- adatao.sql("SELECT * FROM test LIMIT 50")
  expect_identical(paste0(rows[1,],collapse=","), "238,val_238")
  ret <- adatao.sql("SELECT count(*) FROM test")
  expect_identical(ret, 500)
})

test_that("LoadHiveTable works", {
  adatao.sql("drop table if exists test")
  adatao.sql("CREATE TABLE test (uid INT, type STRING)")
  adatao.sql("LOAD DATA LOCAL INPATH '${hiveconf:shark.test.data.path}/kv3.txt' INTO TABLE test")
  df <- adatao.loadHiveTable(table_name="test")
  expect_match(df@id, "[a-z0-9]{8}\\-[a-z0-9]{4}\\-[a-z0-9]{4}\\-[a-z0-9]{4}\\-[a-z0-9]{12}")
  expect_equivalent(colnames(df), c("uid","type"))
  expect_equivalent(df@env$coltypes, c("integer","character"))
})

adatao.disconnect()