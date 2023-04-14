#' A function
#'
#' @param directory A directory path
#'
#' @return The dataframe with the read files in directory
#' @importFrom magrittr %>%
#' @ImportFrom dplyr full_join
#' @export

# IMPORTING LIBRARIES
library(tidyverse)
library(readr)
library(magrittr)
library(purrr)
library(dplyr)

# FUNCTIONS

open_dataset <- function(directory) {
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