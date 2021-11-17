# Simulate ETAS models

library(bayesianETAS)
library(PtProcess)

# Number of simulations per family
N = 100

# Duration of catalog
T <- 852
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

# List of families
families = list.files("../data/Chestler_2017/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

# Loop on families
for (i in 1:1){ #length(families)){
  
  catalog = families[i]
  
  # Open posterior distribution
  output_dir <- paste("models_Chestler_2017/", catalog, sep="")
  readRDS(file = paste(output_dir, "/model_bayesianETAS.rds", sep=""))
  readRDS(file = paste(output_dir, "/posterior.rds", sep=""))

  # Get b-value for Gutemberg-Richter
  beta = model$params[6]

  # Loop on simulations
  for (j in 1:1){ #N){
    
    # Generate random number
    k = floor(dim(posterior)[1] * runif(1))
    mu = posterior[k, 1]
    K = posterior[k, 2]
    alpha = posterior[k, 3]
    c = posterior[k, 4]
    p = posterior[k, 5]

    # Simulate model
    A = K * (p - 1) / c
    params = c(mu, A, alpha, c, p, beta)
    x <- mpp(data=NULL,
             gif=etas_gif,
             mark=list(dmagn_mark, rmagn_mark),
             params=params,
             TT=TT,
             gmap=expression(params[1:5]),
             mmap=expression(params))
    x <- simulate(x, seed=5)
#    simulation <- simulateETAS(mu, K, alpha, c, p, beta, 0, T, TRUE)
  }
}