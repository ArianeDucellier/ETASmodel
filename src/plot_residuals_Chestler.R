# Script to plot fitted ETAS gif and residuals

families = list.files("../data/Chestler_2017/catalogs", pattern="*.txt")
families = gsub(".txt", "", families)

# Loop on families
for (i in 1:length(families)){
  
  catalog = families[i]
  
  # Open posterior distribution
  output_dir <- paste("models_Chestler_2017/", catalog, sep="")
  model <- readRDS(file = paste(output_dir, "/model_PtProcess.rds", sep=""))
  