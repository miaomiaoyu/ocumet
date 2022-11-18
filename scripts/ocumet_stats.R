#install.packages(c("ggplot2", "ggpubr", "tidyverse", "broom", "AICcmodavg"))

library(ggplot2)
library(ggpubr)
library(tidyverse)
library(broom)
library(AICcmodavg)

# set working directory
setwd("~/Documents/LiaoLab/ocumet")

# load data
ocumet.data <- read.csv("./data/ocumet-1102-clean.csv",
                        header = TRUE)

summary(ocumet.data)
