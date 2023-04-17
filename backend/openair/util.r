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
library(collections)

# FUNCTIONS

read_dataframe <- function(filename) {
    df <- read_csv(filename,
    na = c(" ", "nan"),
    locale = readr::locale(encoding = "latin1")
    )

    # convert date objects
    df$date <- as.POSIXct(
        strptime(df$date, format = "%d/%m/%Y %H:%M")
        )

    print(df)
    return(df)
}

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

    df <- tempfile()
    # READING FILES AND STORING THEM INTO THE ABOVE LIST
    for (i in seq(1, length(list_files))) {

        if (i == 0) {
            # reading first df
            df <- read_dataframe(list_files[i])

        } else {
            # reading new df
            csv_obj <- read_dataframe(list_files[i])

            # MERGING THE DATAFRAMES
            intersect <- intersect(colnames(df), colnames(csv_obj))
            print(df)
            df <- merge(
                df,
                csv_obj,
                by = intersect,
                all = TRUE)
        }
    }

    # RETURN RESULT
    return(df)
}

handle_args <- function(parsed_args) {
    n <- length(parsed_args)
    d <- dict() # empty dict
    if (n > 2) {
        for (i in seq(1, n, 2)) {
            arg_n <- nchar(parsed_args[i])
            d$set(substr(parsed_args[i], 3, arg_n), parsed_args[i + 1])
        }
    }

    # retorna o dicionario
    return(d)
}