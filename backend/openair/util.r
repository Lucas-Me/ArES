#' @importFrom magrittr %>%

# IMPORTING LIBRARIES
library(openair)
library(tidyverse)
library(readr)
globalVariables(c("mpg", "hp", "mpg_div_hp"))

open_dataset <- function(directory = "C:\\Users\\lucassm\\.ArES\\temp") {
    # LISTING EXISTING FILES
    list_files <- list.files(
        path = directory, pattern = "*.csv",
        all.files = FALSE,
        full.names = TRUE,
        recursive = FALSE,
        ignore.case = FALSE,
        include.dirs = FALSE,
        no.. = FALSE
        )

    # CREATING EMPTY LIST
    df_list <- list()

    # READING FILES AND STORING THEM INTO THE ABOVE LIST
    for (i in seq(1, length(list_files))){
        csv_obj <- read_csv(list_files[i],
        na = c(" ", "nan"),
        locale = readr::locale(encoding = "latin1")
        )
        # convert date objects
        csv_obj$date <- as.POSIXct(
            strptime(csv_obj$date, format = "%d/%m/%Y %H:%M")
            )

        # appending
        df_list <- append(df_list, list(csv_obj))
    }

    # MERGING INTO ONE SINGLE DATAFRAME
    df <- df_list %>% reduce(full_join, by = c("site", "date"))

    # RETURN RESULTS
    return(df)
}


# OPTIONS TO SAVE FIGURE
# png(file.path(directory, "teste.png"),
#     width = 8, height = 4, units = "in", res = 300)

# CUSTOM COMMANDS NEED TO BE INSERTED HERE
# timeVariation(df, pollutant = c("pm10", "pts"),
# ylab = "pm10 (µg/m3)")

# CLOSE AND SAVE FIGURE
# dev.off() #only 129kb in size