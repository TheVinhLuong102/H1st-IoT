library(adatao)
context("ThriftClient")

test_that("Connect and disconnect commands work", {
  adatao.connect("localhost", 7911)
  expect_is(adatao:::.adataoEnv[["cli"]], "ThriftClient")
  cli <- adatao:::.adataoEnv[["cli"]]
  expect_true(!is.null(adatao:::.adataoEnv[["sid"]]))
  adatao.disconnect()
  expect_true(is.null(adatao:::.adataoEnv[["cli"]]))
  expect_true(is.null(adatao:::.adataoEnv[["sid"]]))
}) 

test_that("Multi-user support work", {
  adatao.connect("localhost", 7911)
  expect_is(adatao:::.adataoEnv[["cli"]], "ThriftClient")
  cli <- adatao:::.adataoEnv[["cli"]]
  expect_equal(cli@nhost, "localhost")
  expect_true(cli@nport > 7911)
  expect_true(!is.null(adatao:::.adataoEnv[["sid"]]))
  adatao.showTables()
  adatao.disconnect()
  expect_true(is.null(adatao:::.adataoEnv[["cli"]]))
  expect_true(is.null(adatao:::.adataoEnv[["sid"]]))
})