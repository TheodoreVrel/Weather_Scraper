# Step 1: Load necessary libraries
library(dplyr)
library(tidyr)
library(ggplot2)

clean_data <- function(filepath) {
  print(paste("Cleaning data in:", filepath))
  
  # Step 2: Read the CSV file
  df <- read.csv(filepath)
  
  # Remove all occurrences of -100 in the dataset (default value when not found)
  df[df == -100] <- NA
  
  # Remove duplicate rows
  df <- df[!duplicated(df), ]
  
  df <- df[, !grepl("diff$", colnames(df))]
  
  print(df)
  
  print("Data cleaned. Writing back to CSV...")
  write.csv(df, filepath, row.names = FALSE)
  print("Cleaning complete.")
}

# Define column groups for comparison
compare_columns <- list(
  c("f_i_resort_snow", "s_i_resort_snow", "a_resort_snow"),
  c("f_i_altitude_snow", "s_i_altitude_snow", "a_altitude_snow"),
  c("f_i_resort_temp", "s_i_resort_temp", "a_resort_temp"),
  c("f_i_altitude_temp", "s_i_altitude_temp", "a_altitude_temp")
)

# Function to perform comparisons
compare_data <- function(df, cols) {
  print(paste("Processing comparison for:", paste(cols, collapse = ", ")))
  
  # Check if at least two columns exist (to perform a meaningful comparison)
  existing_cols <- cols[cols %in% colnames(df)]
  if (length(existing_cols) < 2) {
    print(paste("Skipping comparison, not enough columns found:", paste(existing_cols, collapse = ", ")))
    return(df)  # Return unchanged dataframe
  }
  
  # Generate new column names
  base_col <- cols[1]
  diff_fi_si_name <- paste0(base_col, "_vs_", cols[2], "_diff")  # Custom naming
  diff_fi_a_name <- ifelse(length(cols) == 3, paste0(base_col, "_vs_", cols[3], "_diff"), NA)
  
  
  # Compute differences, allowing NA values to propagate
  if (!(diff_fi_si_name %in% colnames(df))) {
    if (all(c(cols[1], cols[2]) %in% colnames(df))) {
      df[[diff_fi_si_name]] <- df[[cols[1]]] - df[[cols[2]]]
    } else {
      df[[diff_fi_si_name]] <- NA  # Create the column with NA if missing
    }
  }
  
  if (!is.na(diff_fi_a_name) && !(diff_fi_a_name %in% colnames(df))) {
    if (length(cols) == 3 && all(c(cols[1], cols[3]) %in% colnames(df))) {
      df[[diff_fi_a_name]] <- df[[cols[1]]] - df[[cols[3]]]
    } else {
      df[[diff_fi_a_name]] <- NA  # Create the column with NA if missing
    }
  }
  
  return(df)
}

# Function to load, process, and overwrite the CSV file
process_csv <- function(file_path) {
  print(paste("Processing file:", file_path))
  
  clean_data(file_path)
  df <- read.csv(file_path, stringsAsFactors = FALSE)
  
  # Apply comparison function to each group
  for (cols in compare_columns) {
    df <- compare_data(df, cols)
  }
  
  print("Writing updated data to CSV...")
  write.csv(df, file_path, row.names = FALSE)
  print("Processing complete.")
}


folder_path <- "../station_csv_files"

# Get a list of all CSV files in the folder
csv_files <- list.files(path = folder_path, pattern = "\\.csv$", full.names = TRUE)

for (file in csv_files) {
  process_csv(file)
}
Sys.sleep(2)


