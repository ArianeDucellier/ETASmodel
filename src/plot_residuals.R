# Script to plot the residuals of the ETAS models
# and check the goodness of fit

library(PtProcess)

# List of families
families = list.files("../data/Chestler_2017/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

TT <- c(0, 852)

# Functions for the magnitude/frequency law
dmagn_mark <- function(x, data, params){
  y <- dexp(x[, "magnitude"], rate=params[6], log=TRUE)
  return(y)
}
rmagn_mark <- function(ti, data, params){
  y <- rexp(1, rate=params[6])
  return(list(magnitude=y))
}
expmap <- function(y, p){
  y$params[1:5] <- exp(p)
  return(y)
}

# Loop on families
for (i in 1:length(families)){
  
  catalog = families[i]
  output_dir <- paste("models_Chestler_2017/", catalog, sep="")

  # Read data
  filename = paste("../data/Chestler_2017/catalogs/", catalog, ".txt", sep="")
  data = read.table(filename, header=TRUE)
  
  params <- c(0.05, 5.2, 1.8, 0.02, 1.1, 1/mean(data$magnitude))
  
  x <- mpp(data=data, gif=etas_gif,
           mark=list(dmagn_mark, rmagn_mark),
           params=params, TT=TT,
           gmap=expression(params[1:5]),
           mmap=expression(params))

  z = readRDS(file = paste(output_dir, "/model_PtProcess.rds", sep=""))
  x0 <- expmap(x, z$estimate)

  gif<- etas_gif(data, c(0:TT[2]), x0$params)
  res <- residuals(x0)

  filename = paste(output_dir, "/gif.txt", sep="")
  write.table(gif, filename, quote=FALSE, row.names=FALSE, col.names=FALSE)

  filename = paste(output_dir, "/res.txt", sep="")
  write.table(res, filename, quote=FALSE, row.names=FALSE, col.names=FALSE)
}
