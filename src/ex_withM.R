catalog = read.table("../data/Chestler_2017/catalogs/2009.9.11.0.11.15.txt")

dmagn_mark <- function(x, data, params){
  y <- dexp(x[,"magnitude"], rate=params[6], log=TRUE)
  return(y)
}

rmagn_mark <- function(ti, data, params){
  y <- rexp(1, rate=params[6])
  return(list(magnitude=y))
}

TT <- c(0, 852)
params <- c(0.05, 5.2, 1.8, 0.02, 1.1, 1/mean(catalog$magnitude))

x <- mpp(data=catalog, gif=etas_gif,
         mark=list(dmagn_mark, rmagn_mark),
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
