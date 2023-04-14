# IMPORTING LIBRARIES
library(openair)

# IMPORTING SOURCE SCRIPTS
source(".\\backend\\openair\\util.r")

# OPEN DATASET
directory <- "C:\\Users\\lucassm\\.ArES\\temp"
df <- open_dataset(directory)
print(df)

# OPTIONS TO SAVE FIGURE
png(file.path(directory, "teste.png"),
    width = 8, height = 4, units = "in", res = 300)

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
timeVariation(df, pollutant = c("o3", "so2"),
ylab = "µg/m3")

# CLOSE AND SAVE FIGURE
dev.off() #only 129kb in size