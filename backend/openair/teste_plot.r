# IMPORTING LIBRARIES
library(openair)

# IMPORTING SOURCE SCRIPTS
source(".\\backend\\openair\\util.r")

# COMMON ENTRY ARGS
# [fname, inputdir, dpi, figwidth, figheight, sites, parameters]
args <- handle_args(commandArgs(trailingOnly = TRUE))

# OPEN DATASET
df <- open_dataset(args$get("inputdir"))

# OPTIONS TO SAVE FIGURE
png(
    args$get("fname"),
    width = strtoi(args$get("figwidth", 8)),
    height = strtoi(args$get("figheight", 5)),
    units = "in",
    res = strtoi(args$get("dpi", 200))
    )

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
timeVariation(
    df,
    pollutant = c("pts", "pm10"),
    ylab = "µg/m3",
    # name.pol = c(),
    # normalize = FALSE,
    # group = "site",
    # cols = c(),
    xlab = c("Hora", "Hora", "Mês", "Dia da semana"), # Fixed
)

# CLOSE AND SAVE FIGURE
dev.off() #only 129kb in size