library(openair)
library(tibble)
mydata <- read.csv("C:\\Users\\lucassm\\.ArES\\temp\\XS_ST.csv",
    header = TRUE,
    na.strings = c("NA", "NaN", " ", "nan"))
mydata$date <- as.POSIXct(strptime(mydata$date, format = "%d/%m/%Y %H:%M",
"GMT"))
