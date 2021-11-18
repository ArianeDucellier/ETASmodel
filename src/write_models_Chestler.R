# Scripts to write model results in file

families = list.files("../data/Chestler_2017/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

df <- data.frame(matrix(ncol = 7, nrow = 0))
colnames(df) <- c("family", "mu", "A", "c", "p", "alpha", "beta")

# Loop on families
for (i in 1:length(families)){
  
  catalog = families[i]
  
  # Open posterior distribution
  output_dir <- paste("models_Chestler_2017/", catalog, sep="")
  model <- readRDS(file = paste(output_dir, "/model_bayesianETAS.rds", sep=""))
  posterior <- readRDS(file = paste(output_dir, "/posterior.rds", sep=""))
  mu <- model$params[1]
  A <- model$params[2] * (model$params[5] - 1) / model$params[4]
  alpha <- model$params[3]
  c <- model$params[4]
  p <- model$params[5]
  beta <- model$params[6]
  df[i,] <- c(catalog, mu, A, c, p, alpha, beta)
  output_file <- paste(output_dir, "/posterior.txt", sep="")
  write.table(posterior, output_file, row.names=FALSE, col.names=FALSE)
}
write.table(df, file="models_Chestler_2017.txt", quote=FALSE, row.names=FALSE)
