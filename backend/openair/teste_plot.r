# IMPORTING LIBRARIES
library(openair)

# IMPORTING SOURCE SCRIPTS
source(".\\backend\\openair\\util.r")

# COMMON ENTRY ARGS
# [fname, inputdir, dpi, figwidth, figheight, sites, parameters]
args <- handle_args(commandArgs(trailingOnly = TRUE))

# OPEN DATASET
df <- open_dataset(args$get("inputdir"))

# FILTER BY SITE
sites <- string2vector(args$get("sites"))
df <- filter(df, df$site %in% sites)
group_site <- length(sites) > 1 # is it necessary to group by site?

# FILTER BY PARAMETER
parameters <- string2vector(args$get("parameters"))
# if (length(parameters) == 1) {
#     parameters <- parameters[1]
# }

# OPTIONS TO SAVE FIGURE
png(
    args$get("fname"),
    width = strtoi(args$get("figwidth", 8)),
    height = strtoi(args$get("figheight", 5)),
    units = "in",
    res = strtoi(args$get("dpi", 200))
    )

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
if (group_site) {
    timeVariation(
        df,
        pollutant = parameters,
        ylab = "µg/m3",
        # name.pol = c(),
        # normalize = FALSE,
        group = "site",
        # cols = c(),
        xlab = c("Hora", "Hora", "Mês", "Dia da semana"), # Fixed
    )
} else {
    timeVariation(
        df,
        pollutant = parameters,
        ylab = "µg/m3",
        # name.pol = c(),
        # normalize = FALSE,
        # cols = c(),
        xlab = c("Hora", "Hora", "Mês", "Dia da semana"), # Fixed
    )
}

# CLOSE AND SAVE FIGURE
dev.off() #only 129kb in size