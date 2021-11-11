# Read LFE catalog and compute ETAS model

families = list.files("../data/Sweet_2014/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

# Second method: Use package PtProcess
library(PtProcess)

# Functions
expmap <- function(y, p){
    y$params[1:5] <- exp(p)
    return(y)
}

# Start second method
TT <- c(0, 1803)

for (i in 1:length(families)){
    
    catalog = families[i]
    output_dir <- paste("models_Sweet_2014/", catalog, sep="")
    if (!dir.exists(output_dir)){
        dir.create(output_dir)
    }

    # Read data
    filename = paste("../data/Sweet_2014/catalogs/", catalog, ".txt", sep="")
    data = read.table(filename, header=TRUE)

    params <- c(0.05, 5.2, 1.8, 0.02, 1.1)
    
    x <- mpp(data=data, gif=etas_gif,
             mark=list(NULL, NULL),
             params=params, TT=TT,
             gmap=expression(params[1:5]),
             mmap=expression(params))
    
    # First optimization to find starting point
    initial <- log(params[1:5])
    z <- optim(initial, neglogLik, object=x, pmap=expmap, control=list(trace=1, maxit=100))
    
    # Second optimization to get better fit
    initial <- z$par
    z <- nlm(neglogLik, initial, object=x, pmap=expmap, print.level=2, iterlim=500, typsize=initial)
    
    # Save model in files
    saveRDS(z, file = paste(output_dir, "/model_PtProcess.rds", sep=""))
}
