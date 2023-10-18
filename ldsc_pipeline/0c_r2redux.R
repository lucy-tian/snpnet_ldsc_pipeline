library(r2redux)
library(devtools)
library(dplyr)

fullargs <- commandArgs(trailingOnly = FALSE)
args <- commandArgs(trailingOnly = TRUE)


phenotypes = readLines("phenotypes.txt")
df_list <- list()
for (p in phenotypes) {
    filename <- paste0("sscore_by_pheno/", as.character(arg[1]), "_", p, "_input.tsv")
    data <- read.delim(filename, sep="\t", header=TRUE)
    output1=r2_diff(data,c(1),c(3),nrow(data))
    output2=r2_diff(data,c(2),c(3),nrow(data))
    output3=r2_diff(data,c(1),c(2),nrow(data))
    df1 <- data.frame(output1)
    df1$Phenotype <- c(p)
    df1$compare_to <- c("base")
    df2 <- data.frame(output2)
    df2$Phenotype <- c(p)
    df2$compare_to <- c("ukbb")
    df3 <- data.frame(output3)
    df3$Phenotype <- c(p)
    df3$compare_to <- c("ukbb_base")
    df_list <- append(df_list, list(df1))
    df_list <- append(df_list, list(df2))
    df_list <- append(df_list, list(df3))
    
    }

df_all <- bind_rows(df_list)
write.csv(df_all, paste0("sscore_by_pheno/", as.character(arg[1]), "_p_val_significance.csv"), row.names = FALSE)