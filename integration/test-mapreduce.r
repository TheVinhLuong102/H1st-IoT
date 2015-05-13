library(adatao)
context("MapReduce")
# All of those tests run OK on spark local standalone cluster mode
test_that("Wordcount works", {
  adatao.connect("localhost", 7911)
  
  map_func = function(k, line) {
    lapply( strsplit(x=line, split=' ')[[1]], function(w) list(k=w, v=1) ) 
  }
  reduce_func = function(k, values) {
    res <- 0
    n <- length(values)
    for (i in 1:n) {
      res <- res + as.integer(values[i])
    }
    as.character(res)
  }
  
  adatao.mapreduce.to.hdfs("resources/input", "resources/output", map=map_func,reduce=reduce_func)
  df<-adatao.loadTable("resources/output", ",")
  rows <- adatao.sample(df, 1, seed=123)
  expect_identical(paste0(rows,collapse=","),"123.34,3")
  adatao.disconnect()
})
          
test_that("Planage works", {
  adatao.connect("localhost", 7911)
  
  map_func = function(k, line) {
    fields <- unlist(strsplit(line, split=','))
    res <- list(list(k=fields[11], v=line))
    res
  }
  reduce_func = function(k, values) {
    res <- 0
    n <- length(values)
    month <- rep(NA, n)
    for (i in 1:n) {
      items <- unlist(strsplit(values[i], ","))
      month[i] <- as.integer(items[1]) * 12  + as.integer(items[2])
    }
    birthPlane <- min(month)
    planeage <- rep(NA, n)
    fightNo <- rep(NA, n)
    for (i in 1:n) {
      items <- unlist(strsplit(values[i], ","))
      planeage[i] <- as.integer(items[1]) * 12  + as.integer(items[2]) - birthPlane
      fightNo[i] <- items[10]
    }
    res <- paste(fightNo, planeage,collapse="|", sep=":")
  }
  adatao.mapreduce.to.hdfs("resources/airline.csv", "resources/output", map=map_func,reduce=reduce_func)
  df<-adatao.loadTable("resources/output", ",")
  rows <- adatao.sample(df, 1, seed=123)
  expect_identical(paste0(rows[1,],collapse=","),"N772SW,3231:0")
  adatao.disconnect()
})
          
test_that("Airlines works", {
  adatao.connect("localhost", 7911)
  
  map_func = function(k, line) {
    fields <- unlist(strsplit(line, "\\,"))
    # Skip header lines and bad records:
    if (!(identical(fields[[1]], "Year")) & length(fields) == 29) {
      deptDelay <- fields[[16]]
      # Skip records where departure delay is "NA":
      if (!(identical(deptDelay, "NA"))) {
        # field[9] is carrier, field[1] is year, field[2] is month:
        list(list(k=paste(fields[[9]], fields[[1]], fields[[2]],sep=","), v=paste(deptDelay,1,sep=",")))
      }
    }
  }
  
  reduce_func = function(key, values) {
    totaldept <- 0
    count <- 0
    for (i in 1:length(values)) {
      fields <- unlist(strsplit(values[i], "\\,"))
      totaldept <- totaldept + as.numeric(fields[[1]])
      count <- count + as.numeric(fields[[2]])
    }
    paste(totaldept, count, sep=";")
  }
  adatao.mapreduce.to.hdfs("resources/airline.csv", "resources/output", map=map_func,reduce=reduce_func)
  
  df<-adatao.loadTable("resources/output", ",")
  rows <- adatao.sample(df, 1, seed=123)
  expect_identical(paste0(rows,collapse=","),"WN,2008,6,8;2")
  adatao.disconnect()
})

test_that("partition.rand works", {
  pp <- partition.rand(mtcars)
  expect_equal(length(pp), 2)
  expect_equal(nrow(pp[[1]]) + nrow(pp[[2]]), 32)
})

test_that("partition.range works", {
  pp <- partition.range(mtcars)
  expect_equal(length(pp), 2)
  expect_equal(nrow(pp[[1]]), 16)
  expect_equal(nrow(pp[[2]]), 16)
})

test_that("keyval.row works", {
  kv <- keyval.row(1, 2)
  expect_equal(is.adatao.1d.kv(kv), T)
  expect_equal(is.adatao.kv(kv), T)
  
  # ok cases
  keyval.row(1, 1:11)
  keyval.row("global", list(1, 2, 3))
  keyval.row("K", list(a=1, b=2, c=3))
  
  # error cases
  expect_error(keyval.row(1:10, 1:11), "must be a scalar value")
  expect_error(keyval.row(matrix(1, 10, 10), 1:100), "must be a scala value, not n-dimensional")
  expect_error(keyval.row(list(a=1, b=2), 1:100), "must be .* scalar")
})

test_that("keyval works", {
  kv <- keyval(1:10, 1:10)
  expect_equal(is.adatao.1d.kv(kv), F)
  expect_equal(is.adatao.kv(kv), T)
  
  # ok cases
  keyval(1:10, 101:110)
  keyval(1:10, seq(10, 100, by = 10))
  keyval(1:32, mtcars)
  keyval(rep("global", nrow(mtcars)), mtcars)
  keyval(mtcars$gear, mtcars)
  keyval(mtcars$gear, mtcars$wt)
  keyval(mtcars$gear, data.frame(mtcars$wt, mtcars$hp))
  keyval(mtcars$gear, mtcars[, c('wt', 'hp')])
  keyval(airquality$Month, airquality)
  keyval(ToothGrowth$dose, ToothGrowth[, c('len', 'supp')])
  
  # error cases
  expect_error(keyval(1:10, 1:11), "must match in length")
  expect_error(keyval(1, 1:11), "must match in length")
  expect_error(keyval(matrix(1, 10, 10), 1:100), "must be one-dimensional")
  expect_error(keyval(list(a=1, b=2), 1:100), "must be .* atomic")
})

test_that("mapreduce.local works for scalar key & value", {
  sumhp <- mapreduce.local(partition.rand(mtcars),
                           function(part) {
                             keyval(key=part$gear, val=part$hp) },
                           function(key, vv) {
                             keyval.row(key=key, val=sum(vv)) },
                           T, F)
  expect_equal(sumhp$val, aggregate(hp~gear, mtcars, FUN=sum)$hp)
})

test_that("mapreduce.local works for scalar key & value, mapside.combine=F", {
  sumhp <- mapreduce.local(partition.rand(mtcars),
                           function(part) {
                             keyval(key=part$gear, val=part$hp) },
                           function(key, vv) {
                             keyval.row(key=key, val=sum(vv)) },
                           F, F)
  expect_equal(sumhp$val, aggregate(hp~gear, mtcars, FUN=sum)$hp)
})

test_that("mapreduce.local works for scalar key & data.frame value", {
  res <- mapreduce.local(partition.rand(mtcars),
                         function(part) {
                           keyval(key=rep("global", nrow(part)),
                                  val=part[, c('wt', 'hp')]) },
                         function(key, vv) {
                           keyval.row(key=key,
                                      val=list(wt=sum(vv$wt), hp=sum(vv$hp))) },
                         T, F)
  expect_equal(class(res), "data.frame")
  expect_equal(res$key, "global")
  expect_equal(res$wt, sum(mtcars$wt))
  expect_equal(res$hp, sum(mtcars$hp))
})

test_that("mapreduce.local works for scalar key & data.frame value, mapside.combine=F", {
  res <- mapreduce.local(partition.range(mtcars),
                         function(part) {
                           keyval(key=rep("global", nrow(part)),
                                  val=part[, c('wt', 'hp')]) },
                         function(key, vv) {
                           keyval.row(key=key,
                                      val=list(wt=sum(vv$wt), hp=sum(vv$hp))) },
                         T, F)
  expect_equal(class(res), "data.frame")
  expect_equal(res$key, "global")
  expect_equal(res$wt, sum(mtcars$wt))
  expect_equal(res$hp, sum(mtcars$hp))
})

test_that("mapreduce.local works for scalar key & vector reduce value, a la kmeans", { 
  # same for both partition, for deterministic purpose, otherwise should sample()
  clusterid <- c(3, 2, 2, 1, 1, 1, 2, 2, 1, 3, 2, 2, 2, 1, 1, 1)
  res <- mapreduce.local(partition.range(mtcars),
                         function(part) {
                           keyval(key=clusterid,
                                  val=part[, c('mpg', 'wt', 'hp', 'qsec')]) },
                         function(key, vv) {
                           keyval.row(key=key,
                                      val=apply(vv, 2, mean)) },
                         F, F)
  expect_equal(class(res), "data.frame")
})

test_that("mapreduce.local works, user can filter NA", {
  res <- mapreduce.local(partition.rand(airquality),
                         function(part) {
                           part <- part[!is.na(part$Solar.R) & !is.na(part$Ozone), ]
                           part$Diff <- part$Solar.R - part$Ozone
                           keyval(key=part$Month, val=part$Diff) },
                         function(key, vv) {
                           keyval.row(key=key, val=list(sum=sum(vv), count=nrow(vv))) },
                         F, F)
  expect_equal(class(res), "data.frame")
})

test_that("mapreduce.local works, heterogenous map values", {
  res <- mapreduce.local(partition.rand(ToothGrowth),
                         function(part) {
                           part$supp <- as.numeric(part$supp)
                           keyval(key=part$dose, val=part[, c('len', 'supp')]) },
                         function(key, vv) {
                           keyval.row(key=key, val=list(len=sum(vv$len), supp=mean(vv$supp))) },
                         F, F)
  expect_equal(class(res), "data.frame")
  expect_equal(res$key, c("0.5", "1", "2"))
  expect_equal(res$len, c(212.1, 394.7, 522.0))
  expect_equal(res$supp, c(1.5, 1.5, 1.5))
})

test_that("mapreduce.local works, multiple keyval() output in reduce.func", {
  res <- mapreduce.local(partition.range(mtcars),
                         function(part) {
                           keyval(part$gear, part)
                         },
                         function(k, vv) {
                           df <- vv
                           df$row.count <- nrow(vv)
                           keyval(key=rep(k, nrow(vv)), val=df);
                         },
                         mapside.combine = F, F)
  expect_equal(class(res), "data.frame")
  expect_equal(ncol(res), 13)
  expect_equal(res$row.count, c(15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,12,12,12,12,12,12,12,12,12,12,12,12,5,5,5,5,5))
})

#' these tests the internally used functions,
#' you must use devtools "Load All" and run manually
test_internal <- function() {
  test_that("rbind.vv works", {
    df <- rbind.vv(list(123))
    expect_equal(class(df), "data.frame")
    expect_equal(names(df), c("val"))
    
    df2 <- rbind.vv(list(123, 456))
    expect_equal(class(df2), "data.frame")
    expect_equal(names(df2), c("val"))
    expect_equal(df2$val, c(123, 456))
    
    df3 <- rbind.vv(list(list(sum=12, count=1)))
    expect_equal(class(df3), "data.frame")
    expect_equal(names(df3), c("sum", "count"))
    expect_equal(df3$sum, c(12))
    expect_equal(df3$count, c(1))
    
    df4 <- rbind.vv(list(list(a=123, b=456), list(a=246, b=357)))
    expect_equal(class(df4), "data.frame")
    expect_equal(names(df4), c("a", "b"))
    expect_equal(df4$a, c(123, 246))
    expect_equal(df4$b, c(456, 357))
    
    df5 <- rbind.vv(list(list(123, 456), list(246, 357)))
    expect_equal(class(df5), "data.frame")
    expect_equal(names(df5), c("val1", "val2"))
    expect_equal(df5$val1, c(123, 246))
    expect_equal(df5$val2, c(456, 357))
    
    oldOpt <- getOption("stringsAsFactors")
    options(stringsAsFactors = F)
    
    df6 <- rbind.vv(list(data.frame(list(x=1, y=2, z="3")),
                         data.frame(list(x=10, y=20, z="30"))))
    expect_equal(class(df6), "data.frame")
    expect_equal(names(df6), c("x", "y", "z"))
    expect_equal(df6$x, c(1, 10))
    expect_equal(df6$y, c(2, 20))
    expect_equal(df6$z, c("3", "30"))
    
    options(stringsAsFactors = oldOpt)
  })
}