# IMPORTING LIBRARIES
library(openair)

# IMPORTING SOURCE SCRIPTS
source(".\\backend\\openair\\util.r")

# COMMON ENTRY ARGS
# [fname, inputdir, dpi, figwidth, figheight, sites, parameters]
args <- handle_args(commandArgs(trailingOnly = TRUE))

# OPEN DATASET
df <- open_dataset(args$get("inputdir"))

# GROUP BY DIFFERENT TYPES
types <- c()

# FILTER BY SITE
sites <- string2vector(args$get("sites"))
df <- filter(df, df$site %in% sites)
group_site <- length(sites) > 1 # is it necessary to group by site?
if (group_site) {
    types <- append(types, "site")
}
types <- append(types, "year")

# COLORMAP TO FOLLOW
colors <- string2vector(args$get("colors"))
print(types)

# OPTIONS TO SAVE FIGURE
png(
    args$get("fname"),
    width = strtoi(args$get("figwidth", 8)),
    height = strtoi(args$get("figheight", 5)),
    units = "in",
    res = strtoi(args$get("dpi", 200))
    )

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
if (length(types) > 0) {
    windRose(
        mydata = df,
        paddle = FALSE,
        type = types,
        cols = colors
        )
} else {
    windRose(
        mydata = df,
        paddle = FALSE,
        cols = colors
        )
}

# CLOSE AND SAVE FIGURE
dev.off() #only 129kb in size