### lapply
system.time({save1 <- lapply(1:100, f)})

### mclapply
system.time({save2 <- mclapply(1:100, f)})

### 
system.time(
  {
  cl <- makeCluster(detectCores())
  clusterEvalQ(cl, library(lme4))
  save3 <- parLapply(cl, 1:100, f)
  stopCluster(cl)
}
)



