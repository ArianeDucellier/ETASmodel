catalog = read.table("../data/Chestler_2017/catalogs/2009.9.11.0.11.15.txt")
N <- dim(catalog)[1]
catalog$magnitude <- rep(1, N)

TT <- c(0, 852)
params <- c(0.05, 5.2, 1.8, 0.02, 1.1, 1/mean(catalog$magnitude))

x <- mpp(data=catalog, gif=etas_gif,
         mark=list(NULL, NULL),
         params=params, TT=TT,
         gmap=expression(params[1:5]),
         mmap=expression(params))

expmap <- function(y, p){
  y$params[1:5] <- exp(p)
  return(y)
}

initial <- log(params[1:5])
z <- optim(initial, neglogLik, object=x, pmap=expmap,
           control=list(trace=1, maxit=100))

initial <- z$par
z <- nlm(neglogLik, initial, object=x, pmap=expmap,
         print.level=2, iterlim=500, typsize=initial)

x0 <- expmap(x, z$estimate)
