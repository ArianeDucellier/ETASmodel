# This script reads the simulated catalogs created with
# the ETAS parameter from the catalog of Chestler and Creager (2017)
# and fit an ARFIMA(1, d, 1) on them

library(fracdiff)

families = list.files("../data/Chestler_2017/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

N = 100 # Number of simulations per family
T <- 852 # Number of days in the time series
window = 1 # Duration of time widow to transform catalog into time series

frac_param <- matrix(nrow=N, ncol=length(families))

for (i in 1:length(families)){
 
  catalog = families[i]

  output_dir <- paste("models_Chestler_2017/", catalog, sep="")
  
  for (j in 1:N){
    filename <- paste(output_dir, '/PtProcess/catalog_', j, '.txt', sep="")
    data <- read.table(filename, header=TRUE)
    times = data$times
    ts <- rep(0, T)
    for (k in 1:length(times)){ 
      index <- floor(times[k] / window) + 1
      if ((index >= 1) & (index <= T)){
        ts[index] <- ts[index] + 1
      }
    }
    model <- fracdiff(ts, 1, 1, 0.5, 0.5)
    frac_param[j, i] <- model$d
    print(c(i, j, model$d))
  }
}

write.table(frac_param, "models_Chestler_2017/simulated_d_PtProcess.txt", quote=FALSE, row.names=FALSE, col.names=FALSE)
