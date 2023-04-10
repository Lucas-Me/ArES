# IMPORTING LIBRARIES
library(openair)
library(tidyverse)

# READING AND PREPARING DATA
mydata <- read_csv("C:\\Users\\lucassm\\.ArES\\temp\\SA_BS.csv",
    na = c(" ", "nan"),
    )
mydata$date <- as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M"))

# OPTIONS TO SAVE FIGURE
png("C:\\Users\\lucassm\\.ArES\\temp\\myplot.png",
    width = 8, height = 4, units = "in", res = 100)

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
# summaryPlot(mydata)
timeVariation(mydata, pollutant = "pm10", 
ylab = "pm10 (ug/m3)")

# close figure
dev.off() #only 129kb in size