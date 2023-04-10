
# IMPORTING LIBRARIES
library(openair)
library(tidyverse)

# READING AND PREPARING DATA
mydata <- read_csv("C:\\Users\\lucassm\\.ArES\\temp\\SA_BS.csv",
    na = c(" ", "nan"),
    )
mydata$date <- as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M",
"GMT"))

# CUSTOM COMMANDS NEEDS TO BE INSERTED HERE
x <- summaryPlot(mydata)
x$.Call.graphics()

# OPTIONS TO SAVE FIGURE
# ggsave("C:\\Users\\lucassm\\.ArES\\temp\\SA_BS.png", dpi = 200)