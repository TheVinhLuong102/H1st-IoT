library(adatao)
context("clustering algorithms")
adatao.connect("localhost", 7911)
hdfs_url <- "resources/KmeansData_small"
df <- adatao.loadTable(hdfs_url, sep=" ")

test_that("kmeans numeric columns works", {
  km <- adatao.kmeans(x=df, cols=c(1,2), centers=10, iter.max=10)
  expect_that(nrow(km$centers), equals(10))
  expect_equivalent(km$size, c(1007,1995,466,568,2040,496,896,1022,981,529))
  expect_identical(paste0(format(km$centers[1,]),collapse=","), "2.370852,3.307505")
  expect_identical(paste0(format(km$tot.withinss),collapse=","),"1968780.8, 871227.0, 765868.6, 596472.1, 497577.4, 395854.7, 240458.1, 181978.1, 181809.1, 181807.3")
})

test_that("kmeans character columns works", {
  km <- adatao.kmeans(x=df, c("V1","V2"), centers=10, iter.max=10)
  expect_that(nrow(km$centers), equals(10))
  expect_equivalent(km$size, c(1007,1995,466,568,2040,496,896,1022,981,529))
  expect_identical(paste0(format(km$centers[1,]),collapse=","), "2.370852,3.307505")
  expect_identical(paste0(format(km$tot.withinss),collapse=","),"1968780.8, 871227.0, 765868.6, 596472.1, 497577.4, 395854.7, 240458.1, 181978.1, 181809.1, 181807.3")
})

test_that("kmeans duplicate columns works", {
  km <- adatao.kmeans(x=df, c("V1","V2","V2"), centers=10, iter.max=10)
  expect_that(nrow(km$centers), equals(10))
  expect_equivalent(km$size, c(1007,1995,466,568,2040,496,896,1022,981,529))
  expect_identical(paste0(format(km$centers[1,]),collapse=","), "2.370852,3.307505")
  expect_identical(paste0(format(km$tot.withinss),collapse=","),"1968780.8, 871227.0, 765868.6, 596472.1, 497577.4, 395854.7, 240458.1, 181978.1, 181809.1, 181807.3")
})

test_that("kmeans with initial centers works", {
  centers <- matrix(c(47.981317,26.61045,38.920807,8.66824,6.393636,49.22274), nrow=3)
  km <- adatao.kmeans(x=df, c("V1","V2"), centers=centers, iter.max=10)
  expect_that(nrow(km$centers), equals(3))
  expect_equivalent(km$size, c(2952, 4124, 2924))
  expect_identical(paste0(format(km$centers[1,]),collapse=","), "13.69827,45.29307")
  expect_identical(paste0(format(km$tot.withinss),collapse=","),"3057765,2421456,2069935,1933325,1745109,1603567,1518195,1437590,1356192,1320829")
})

test_that("adatao.predict kmeans works", {
  km <- adatao.kmeans(x=df, cols=c(1,2), centers=10, iter.max=10)
  pred <- adatao.predict(km, df)
  df.pred <- fetchRows(pred, 1)
  expect_identical(paste0(format(df.pred), collapse=","), "23.19896,47.03395,3")
})  

adatao.disconnect()