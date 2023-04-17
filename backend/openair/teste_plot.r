# IMPORTING LIBRARIES
library(openair)

# IMPORTING SOURCE SCRIPTS
source(".\\backend\\openair\\util.r")

# ENTRY ARGS
# [fname, inputdir, dpi, figwidth, figheight, vars]
args <- handle_args(commandArgs(trailingOnly = TRUE))

# # OPEN DATASET
df <- open_dataset(args$get("inputdir"))
print(df)

# # OPTIONS TO SAVE FIGURE
png(
    args$get("fname"),
    width = args$get("figwidth", 8),
    height = args$get("figheight", 5),
    units = "in",
    res = args$get("dpi", 200)
    )

# # CUSTOM COMMANDS NEED TO BE INSERTED HERE
timeVariation(df, pollutant = c("pts", "pm10"),
ylab = "µg/m3")

# # CLOSE AND SAVE FIGURE
dev.off() #only 129kb in size