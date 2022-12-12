#install.packages(c("ggplot2", "ggpubr", "tidyverse", "broom", "AICcmodavg"))

library(ggplot2)
library(ggpubr)
library(tidyverse)
library(broom)
library(AICcmodavg)

# Set working directory
setwd("~/workspace/ocumet")

# Load data
data <- read.csv("data/1209-naion.csv",
                        header = TRUE)

summary(data)
