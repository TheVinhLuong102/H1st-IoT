#!/usr/bin/env Rscript

# magic var for simulating think time
# NA if not set, which mean no pause between commands,
# otherwise pause for a random think time ~ Exponential distribution of lambda, e.g. rexp() in R
pauseRate <- as.double(Sys.getenv("ADATAO_THINK_TIME_LAMBDA"))

bench <- function(HOST, USERNAME, PASSWORD, TABLE, setupCommands, commands, teardownCommands, numIters, doSetupOnce=F, labels=NULL) {
  env <- new.env()
  assign("HOST", HOST, envir=env)
  assign("TABLE", TABLE, envir=env)
  assign("USERNAME", USERNAME, envir=env)
  assign("PASSWORD", PASSWORD, envir=env)
  if (doSetupOnce) sapply(setupCommands, FUN=eval, envir=env)
  
  timing <- matrix(rep(NA, length(commands)*numIters), c(length(commands), numIters))
  
  for (i in 1:length(commands)) {
    if (! doSetupOnce) sapply(setupCommands, FUN=eval, envir=env)
    tryCatch(
      for (j in 1:numIters) {
        cat("Sending request: ", as.character(commands[[i]]), file=stderr())
        timing[[i, j]] <- system.time(eval(commands[[i]], envir=env))[[3]] # elapsed time
        cat("Iteration", j, "of '", as.character(commands[[i]]), "' took", timing[[i, j]], "second\n", file=stderr())
        if (!is.na(pauseRate)) {
          pause <- rexp(1, pauseRate)
          cat("Pausing for", pause, "second...\n", file=stderr())
          Sys.sleep(pause)
        }
      },
      error = function(e) { warning("Command '", as.character(commands[[i]]), "' failed: ", as.character(e), immediate=T) },
      finally = if (! doSetupOnce) { sapply(teardownCommands, FUN=eval, envir=env) }
    )
  }
  
  if (doSetupOnce) sapply(teardownCommands, FUN=eval, envir=env)
  if (is.null(labels)) {
    labels <- commands
  }
  df <- data.frame(timing, row.names=labels)
  
  # write to stdout
  write.csv(df, file="")
  
  # write to file also
  fname <- paste("Benchmark timing table", HOST, USERNAME, TABLE, date(), sep=" - ")
  fname <- paste0(fname, ".csv")
  write.csv(df, file=fname)

  invisible(df)
}

connect <- c(
  quote(adatao.connect(HOST, 16000, USERNAME, PASSWORD)),
  quote(adatao.sql("create table airline (Year int,Month int,DayofMonth int, DayOfWeek int,DepTime int, CRSDepTime int,ArrTime int, CRSArrTime int,UniqueCarrier string, FlightNum int, TailNum string, ActualElapsedTime int, CRSElapsedTime int, AirTime int, ArrDelay int, DepDelay int, Origin string, Dest string, Distance int, TaxiIn int, TaxiOut int, Cancelled int, CancellationCode string, Diverted string, CarrierDelay int, WeatherDelay int, NASDelay int, SecurityDelay int, LateAircraftDelay int ) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','")),
  quote(adatao.sql("LOAD DATA LOCAL INPATH 'integration/airline.csv' INTO TABLE airline"))
)
disconnect <- c(
  quote(adatao.disconnect())
)
airline.load <- c(
  quote(df <- adatao.sql2ddf(paste("select * from ", TABLE)))
)
airline.sample100 <- c(
  quote(df <- adatao.sample2ddf(adatao.sql2ddf(paste("select * from ", TABLE)), 100))
)
# some suite does not need all columns
airline.load14 <- c(
  quote(df <- adatao.sql2ddf(paste("select year, month, dayofmonth, dayofweek, deptime, distance, arrdelay, depdelay, cancelled, carrierdelay, weatherdelay, nasdelay, securitydelay, lateaircraftdelay from ", TABLE)))
)

# this vector of commands should cover all Adatao APIs
all_api_cmds <- c(
  # data extraction
  quote(df[arrdelay==1]),
  quote(df$arrdelay),
  quote(fetchRows(df, 10)),
  quote(fetchRows(df$arrdelay, 10)),
  quote(adatao.sample(df, 20)),
  quote(adatao.sample2ddf(df, 0.001)),

  # data transformation
  #quote(adatao.cut
  #quote(adatao.scale
  quote(adatao.aggregate(arrdelay ~ dayofweek, df, FUN=mean)),
  quote(adatao.as.factor(df, c("dayofweek"))),
  quote(df2 <- adatao.transform(df[arrdelay != 0], logdist=log(arrdelay))),
  quote(adatao.lm(arrdelay ~ dayofweek + depdelay + logdist, data=df2)),
  #quote(adatao.mapreduce

  # data exploration
  #quote(adatao.quantile(df, "arrdelay", c(0.9, 0.95, 0.99))),
  #quote(adatao.fivenum(df)),
  #quote(adatao.fivenum(df$arrdelay)),
  quote(summary(df)),
  quote(summary(df$arrdelay)),
  quote(nrow(df)),
  quote(ncol(df)),
  quote(colnames(df)),
  quote(length(df)),

  quote(adatao.cor(df, "arrdelay", "depdelay")),
  quote(adatao.cov(df, "arrdelay", "depdelay")),
  #quote(adatao.hist(df, "arrdelay", 1000, plot=FALSE)),
  quote(sd(df$arrdelay)),
  quote(mean(df$arrdelay)),
  #quote(var(df$arrdelay)),
  quote(adatao.xtabs(arrdelay ~ dayofweek, df)),
  #quote(adatao.table()),
  #quote(adatao.z.test()),

  # Hive/HDFS

  # pre-ML
  #quote(splits <- adatao.cv.rs(data=df, k=5, seed=42), train <- splits[[1]]$train, test <- splits[[1]]$split),
  quote(splits <- adatao.cv.kfold(data=df, 5, seed=42)),
  quote(train <- splits[[1]]$train),

  quote(test <- splits[[1]]$test),

  # Machine Learning
  ## Regression
  quote(lm1 <- adatao.lm(arrdelay ~ dayofweek + depdelay + uniquecarrier, data=train)),
  quote(lm2 <- adatao.lm.gd(arrdelay ~ dayofweek + depdelay+ uniquecarrier, data=train, learningRate=0.1, numIterations=5)),
  quote(lm3 <- adatao.lm(arrdelay ~ dayofweek + depdelay + uniquecarrier, data=train, regularized="ridge", lambda=2.34)),
  #quote(rf1 <- adatao.randomForest(arrdelay ~ dayofweek + depdelay, data=train, ntree=48, userSeed=452)),

  ## Classification
  quote(glm1 <- adatao.glm(cancelled ~ dayofweek  + depdelay, data=train)),
  quote(glm2 <- adatao.glm(cancelled ~ dayofweek + uniquecarrier + depdelay, data=train)),
  quote(glm3 <- adatao.glm.gd(cancelled ~ dayofweek + depdelay, data=train, learningRate=0.1, numIterations=5)),
  #quote(rf2 <- adatao.randomForest(cancelled ~ dayofweek + depdelay, data=train, ntree=48, userSeed=452)),

  ## Clustering

  quote(km <- adatao.kmeans(train, cols=c("dayofweek", "distance", "arrdelay", "depdelay"), 8, 5)),

  #adatao.fitted
  quote(adatao.residuals(lm1)),

  # post-ML
  quote(pred_lm1 <- adatao.predict(lm1, test)),
  quote(pred_glm1 <- adatao.predict(glm1, test)),
  #quote(pred_rf1 <- adatao.predict(rf1, test)),


  quote(adatao.metrics(pred_glm1)),
  #quote(adatao.metrics(pred_rf1)),

  quote(adatao.binary.confusion.matrix(model=glm1, data=test)),
  quote(adatao.binary.confusion.matrix(model=glm2, data=test)),
  #quote(adatao.binary.confusion.matrix(model=rf1, data=test)),

  quote(adatao.r2(model=lm2, data=test)),
  quote(adatao.r2(model=lm3, data=test)),
  #quote(adatao.r2(model=rf1, data=test)),
  quote(adatao.r2(model=lm1, data=test))
)

#' this serves a standard all-features benchmark
#' or as a full-scale system smoke tests
bench.airline.standard <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(
    connect,
    airline.load
    )
  cmds <- all_api_cmds
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

#' as light weightly as possible to test through all APIs
bench.airline.sample <- function(HOST, USERNAME, PASSWORD, TABLE) {
  before <- c(
    connect,
    airline.sample100
    )
  cmds <- all_api_cmds
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, 1, doSetupOnce=T)
}

bench.airline.load <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  cmds <- c(
    # 7 cols
    quote(adatao.sql2ddf(paste("select year, month, dayofmonth, deptime, distance, arrdelay, depdelay from ", TABLE))),
    # 14 cols
    quote(adatao.sql2ddf(paste("select year, month, dayofmonth, dayofweek, deptime, arrtime, distance, arrdelay, depdelay, carrierdelay, weatherdelay, nasdelay, securitydelay, lateaircraftdelay from ", TABLE))),
    # 29 cols
    quote(adatao.sql2ddf(paste("select * from ", TABLE)))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, connect, cmds, disconnect, numIters, doSetupOnce=F)
}


bench.airline.stats <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  cmds <- c(  
    # basic stats
    quote(nrow(df)),
    quote(sd(df$arrdelay)),
    quote(adatao.quantile(df$arrdelay, c(0.9, 0.95, 0.99))),
    quote(summary(df$depdelay)),
    quote(adatao.fivenum(df$depdelay)),
    quote(summary(df)),
    quote(adatao.fivenum(df)),
    quote(adatao.aggregate(arrdelay ~ month, FUN=mean)),
    quote(adatao.aggregate(depdelay ~ year, FUN=summary)),
    quote(adatao.cor(df$arrdelay, df$depdelay)),
    quote(adatao.as.factor(df, column="cancelled"))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, c(connect, airline.load14), cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.lm.gd <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect, airline.load14, c(
    quote(df <- adatao.as.factor(df, cols=c("year", "month", "dayofmonth", "dayofweek"))),
    quote(df.scaled <- adatao.scale(df, "normalization")),
    quote(splits <- adatao.cv.kfold(data=df.scaled, 3, 42))
  ))
  cmds <- c(
    # lm base
    quote(adatao.lm.gd(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                     data=df.scaled,
                     learningRate=0.25,
                     numIterations=20)),
    
    # lm with 2x iterations
    quote(adatao.lm.gd(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                     data=df.scaled,
                     learningRate=0.25,
                     numIterations=40)),
    
    # lm with x/2 features
    quote(adatao.lm.gd(arrdelay ~ depdelay + weatherdelay + nasdelay,
                    data=df.scaled,
                    learningRate=0.25,
                    numIterations=20)),

    # lm with 12 levels
    quote(adatao.lm.gd(arrdelay ~ month,
                    data=df.scaled,
                    learningRate=0.25,
                    numIterations=20)),

    # lm with 20 levels
    quote(adatao.lm.gd(arrdelay ~ depdelay + month + dayofweek, data=df.scaled, learningRate=0.25, numIterations=20)),

    # lm with 30 levels
    quote(adatao.lm.gd(arrdelay ~ dayofmonth, data=df.scaled, learningRate=0.25, numIterations=20)),
    
    # lm with 49 levels
    quote(adatao.lm.gd(arrdelay ~ month + dayofmonth + dayofweek, data=df.scaled, learningRate=0.25, numIterations=20)),

    # glm.gd
    quote(adatao.glm.gd(cancelled ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                     data=df.scaled,
                     learningRate=0.25,
                     numIterations=20)),

    # glm.gd 30 features
    quote(adatao.glm.gd(cancelled ~ arrdelay ~ dayofmonth, data=df.scaled,
                     data=df.scaled,
                     learningRate=0.25,
                     numIterations=20)),
        
    # lm on cv split
    quote(adatao.lm.gd(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                     data=splits[[1]]$train,
                     learningRate=0.25,
                     numIterations=20))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.linearmodels <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect, airline.load14, c(
    quote(df <- adatao.as.factor(df, cols=c("year", "month", "dayofmonth", "dayofweek"))),
    quote(splits <- adatao.cv.kfold(data=df, k=3, seed=42)),
    quote(df.transformed <- adatao.transform(df[distance != 0], logdist=log(distance)))
  ))
  cmds <- c(
    # lm/glm base 6 features
    quote(adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=df)),
    
    # lm with x/2 features
    quote(adatao.lm(arrdelay ~ depdelay + weatherdelay + nasdelay, data=df)),
    
    # lm with 12 levels
    quote(adatao.lm(arrdelay ~ month, data=df)),
    
    # lm with 20 levels
    quote(adatao.lm(arrdelay ~ depdelay + month + dayofweek, data=df)),

    # lm with 30 levels
    quote(adatao.lm(arrdelay ~ dayofmonth, data=df)),
    
    # lm with 49 levels
    quote(adatao.lm(arrdelay ~ month + dayofmonth + dayofweek, data=df)),
    
    # base lm on cv split
    quote(adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=splits[[1]]$train)),
    
    # base lm on R-transformed feature
    quote(adatao.lm(arrdelay ~ logdist + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=df.transformed)),
    
    # lm/glm with 5-fold cv
    quote(adatao.cv.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                     data=df,
                     k=5, seed=11,
                     regularized="ridge", lambda=1))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.logistic <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect, c(
    quote(df <- adatao.sql2ddf(paste("select year, month, dayofmonth, dayofweek,
                                  deptime, distance, uniquecarrier,
                                  arrdelay, depdelay, if(arrdelay > 7.05, 1, 0) as delayed,
                                  cancelled, 
                                  carrierdelay, weatherdelay, nasdelay, securitydelay, lateaircraftdelay from ", TABLE))),
    quote(df <- adatao.as.factor(df, cols=c("year", "month", "dayofmonth", "dayofweek", "uniquecarrier"))),
    quote(splits <- adatao.cv.kfold(data=df, k=3, seed=42)),
    quote(df.transformed <- adatao.transform(df[distance != 0], logdist=log(distance)))
  ))
  cmds <- c(
    # glm base 6 features
    quote(adatao.glm(cancelled ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                   data=df)),
    
    # with x/2 features
    quote(adatao.glm(cancelled ~ depdelay + weatherdelay + nasdelay, data=df)),
    
    # with 12 levels
    quote(adatao.glm(cancelled ~ month, data=df)),
    
    # with 20 levels
    quote(adatao.glm(cancelled ~ depdelay + month + dayofweek, data=df)),
    
    # with 30 levels
    quote(adatao.glm(cancelled ~ dayofmonth, data=df)),
    
    # with 49 levels
    quote(adatao.glm(cancelled ~ month + dayofmonth + dayofweek, data=df)),
    
    # on cv split
    quote(adatao.glm(cancelled ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                   data=splits[[1]]$train)),
    
    # on R-transformed feature
    quote(adatao.glm(cancelled ~ logdist + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                   data=df.transformed)),
    
    # with 5-fold cv
    quote(adatao.cv.glm(cancelled ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                      data=df,
                      k=5, seed=12,
                      regularized="ridge", lambda=1))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.rddmatrix <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect, airline.load14)
  cmds <- c(
    # lm base
    quote(adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=df)),
    
    quote(adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=df)),
    
    quote(adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                  data=df)),
    
    # lm with categorical var (12 levels)
    quote(adatao.lm(arrdelay ~ month, data=df)),
    
    quote(adatao.lm(arrdelay ~ month, data=df)),
    
    quote(adatao.lm(arrdelay ~ month, data=df))
  )
  labels <- c("lm base 1", "lm base 2", "lm base 3", "lm categorical 1", "lm categorical 2", "lm categorical 3")
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters=2, labels=labels, doSetupOnce=F)
}

bench.airline.kmeans <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  cmds <- c(
    # kmeans base
    quote(adatao.kmeans(df,
                      cols=c("year", 
                             "month",
                             "dayofmonth",
                             "dayofweek",
                             "deptime",
                             "arrdelay",
                             "depdelay"),
                      10,
                      10)),
    
    # kmeans with 2x numIters
    quote(adatao.kmeans(df,
                      cols=c("year", 
                             "month",
                             "dayofmonth",
                             "dayofweek",
                             "deptime",
                             "arrdelay",
                             "depdelay"),
                      10,
                      20)),
    
    # kmeans with 4x numIters
    quote(adatao.kmeans(df,
                      cols=c("year", 
                             "month",
                             "dayofmonth",
                             "dayofweek",
                             "deptime",
                             "arrdelay",
                             "depdelay"),
                            10,
                           40)),  
    
    # kmeans with 4x numClusters
    quote(adatao.kmeans(df,
                      cols=c("year", 
                             "month",
                             "dayofmonth",
                             "dayofweek",
                             "deptime",
                             "arrdelay",
                             "depdelay"),
                      40,
                      10)),
    
    # kmeans with 12x numClusters
    quote(adatao.kmeans(df,
                      cols=c("year", 
                             "month",
                             "dayofmonth",
                             "dayofweek",
                             "deptime",
                             "arrdelay",
                             "depdelay"),
                      120,
                      10))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, c(connect, airline.load14), cmds, disconnect, numIters, doSetupOnce=F)
}

bench.airline.randomForest <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect,
    quote(df <- adatao.sql2ddf(paste("select arrdelay, depdelay, cancelled, carrierdelay, weatherdelay, nasdelay, securitydelay, lateaircraftdelay from ", TABLE)))
  )
  
  cmds <- c(
    # regressor with 100 trees
    quote(regressor100 <- adatao.randomForest(arrdelay ~ cancelled + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                          data=df,
                          mtry=0,
                          ntree=100,
                          userSeed=122)),
    
    # regressor with 1000 trees
    quote(regressor1000 <- adatao.randomForest(arrdelay ~ cancelled + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                          data=df,
                          mtry=0,
                          ntree=1000,
                          userSeed=122))
    
#     # classifier with 100 trees
#     quote(classifier100 <- adatao.randomForest(cancelled ~ arrdelay + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
#                                             data=df,
#                                             mtry=0,
#                                             ntree=100,
#                                             userSeed=122)),
#     
#     # classifier with 1000 trees
#     quote(classifier1000 <- adatao.randomForest(cancelled ~ arrdelay + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
#                                              data=df,
#                                              mtry=0,
#                                              ntree=1000,
#                                              userSeed=122))
  )
    
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.metrics <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  before <- c(connect, airline.load14, c(
    quote(df.scaled <- adatao.scale(df, "normalization")),
    quote(lm1 <- adatao.lm(arrdelay ~ depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                         data=df.scaled)),
    quote(adatao.glm(cancelled ~ deptime + distance + weatherdelay + securitydelay,
                   data=df.scaled,
                   learningRate=0.25,
                   numIterations=20)),
    quote(splits <- adatao.cv.kfold(data=df.scaled, k=3, seed=42)),
    quote(rf_reg <- adatao.randomForest(arrdelay ~ cancelled + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                                      data=splits[[1]]$train,
                                      mtry=0,
                                      ntree=100,
                                      userSeed=122)),
    quote(rf_cls <- adatao.randomForest(cancelled ~ arrdelay + depdelay + carrierdelay + weatherdelay + nasdelay + securitydelay + lateaircraftdelay,
                                      data=splits[[1]]$train,
                                      mtry=0,
                                      ntree=100,
                                      userSeed=122)),
  ))
  cmds <- c(
    # r2
    quote(adatao.r2(lm1, data=df.scaled)),
    
    # r2 on cv split
    quote(adatao.r2(lm1, data=splits[[1]]$test)),
    
    # r2 on train with randomForest
    quote(adatao.r2(rf_reg, data=splits[[1]]$train)),
    
    # r2 on test with randomForest
    quote(adatao.r2(rf_reg, data=splits[[1]]$test)),
    
    # cfm on train with randomForest
    quote(adatao.cfm(rf_cls, data=splits[[1]]$train)),
    
    # cfm on test with randomForest
    quote(adatao.cfm(rf_cls, data=splits[[1]]$test)),
    
    #prediction
    quote(prediction <- adatao.predict(glm1, df.scaled)),
    
    # metric
    quote(adatao.metrics(data=prediction)),
    
    #prediction
    quote(prediction <- adatao.predict(glm1, splits[[3]]$test)),
    
    # metric on cv split
    quote(adatao.metrics(data=prediction))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, before, cmds, disconnect, numIters, doSetupOnce=T)
}

bench.airline.hdfs <- function(HOST, USERNAME, PASSWORD, TABLE, numIters) {
  setup <- c(
    connect,
    quote(df <- adatao.loadTable(TABLE)),
    quote(colnames(df) <- c(
        "year",
        "month",
        "dayofmonth",
        "dayofweek",
        "deptime",
        "crsdeptime",
        "arrtime",
        "crsarrtime",
        "uniquecarrier",
        "flightnum",
        "tailnum",
        "actualelapsedtime",
        "crselapsedtime",
        "airtime",
        "arrdelay",
        "depdelay",
        "origin",
        "dest",
        "distance",
        "taxiin",
        "taxiout",
        "cancelled",
        "cancellationcode",
        "diverted",
        "carrierdelay",
        "weatherdelay",
        "nasdelay",
        "securitydelay",
        "lateaircraftdelay"))
  )
  cmds <- c(
    quote(sd(df$arrdelay)),
    quote(summary(df)),
    quote(adatao.lm(arrdelay ~ depdelay + distance, data=df))
  )
  bench(HOST, USERNAME, PASSWORD, TABLE, setup, cmds, disconnect, numIters, doSetupOnce=F)
}

usage <- function() {
  cat("Usage: Rscript bench.airline.R <section> <adatao_host> <username> <airline_table> <numIters>\n")
  cat("Example:\n")
  cat("    $ Rscript bench.airline.R standard localhost user1 airline_12g 5\n")
  cat("    $ Rscript bench.airline.R linearmodels localhost user2 airline_48g 3\n")
}

argv <- commandArgs(trailingOnly = TRUE)

if (length(argv) < 6) {
  usage()
  stop("Require 6 arguments.")
}

section <- argv[[1]]
host <- argv[[2]]
username <- argv[[3]]
password <- argv[[4]]
table <- argv[[5]]
numIters<- as.integer(argv[[6]])

library(adatao)

options(adatao.debug=T)
options(warn=0)

if (section == "standard") {
  bench.airline.standard(host, username, password, table, numIters)
} else if (section == "sample") {
  bench.airline.sample(host, username, password, table)
} else if (section == "load") {
  bench.airline.load(host, username, password, table, numIters)
} else if (section == "hdfs") {
  bench.airline.hdfs(host, username, password, table, numIters)
} else if (section == "stats") {
  bench.airline.stats(host, username, password, table, numIters)
} else if (section == "lm.gd") {
  bench.airline.lm.gd(host, username, password, table, numIters)
} else if (section == "linearmodels") {
  bench.airline.linearmodels(host, username, password, table, numIters)
} else if (section == "logistic") {
  bench.airline.logistic(host, username, password, table, numIters)
} else if (section == "rddmatrix") {
  bench.airline.rddmatrix(host, username, password, table, numIters)
} else if (section == "kmeans") {
  bench.airline.kmeans(host, username, password, table, numIters)
} else if (section == "metrics") {
  bench.airline.metrics(host, username, password, table, numIters)
} else if (section == "randomForest") {
  bench.airline.randomForest(host, username, password, table, numIters)
} else {
  stop(paste("Invalid benchmark section: ", section,""))
}

warnings()

