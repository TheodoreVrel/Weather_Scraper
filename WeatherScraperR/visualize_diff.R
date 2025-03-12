plot_differences <- function(file_path, temp_or_snow = "", alert_threshold = 0) {
  print(paste("Generating bar plots for:", file_path))
  
  # Load data
  df <- read.csv(file_path, stringsAsFactors = FALSE)
  
  # Identify all difference columns
  diff_cols <- grep(paste0(temp_or_snow, "_diff"), colnames(df), value = TRUE)
  if (length(diff_cols) == 0) {
    print("No difference columns found. Skipping plot generation.")
    return()
  }
  
  # Extract the date from a timestamp column, assuming it exists
  if ("gathered_time_day" %in% colnames(df)) {
    df$Date <- as.Date(df$gathered_time_day)
  } else {
    print("No date column found! Using default ordering.")
    df$Date <- 1  # Assign a dummy value to plot everything as a single batch
  }
  
  # Convert data to long format for ggplot
  long_data <- tidyr::pivot_longer(df, cols = all_of(diff_cols), names_to = "Variable", values_to = "Value")
  long_data <- long_data[!is.na(long_data$Value), ]
  
  threshold <- 5
  if (temp_or_snow == "snow" && alert_threshold == 0){
    threshold <- 10
  }
  if (alert_threshold != 0){
    threshold = alert_threshold
  }
  
  # Create bar plots, one per day
  png(paste0(file_path, "highlighted_bar_graph.png"), width = 800, height = 600)  # Open PNG device
  plot <- ggplot(long_data, aes(x = Variable, y = Value, fill = (Value >= threshold | Value <= -threshold))) +
    geom_bar(stat = "identity", position = "dodge") +
    scale_fill_manual(values = c("FALSE" = "blue", "TRUE" = "red")) +  # Highlight differences ≥ 5
    facet_wrap(~Date, scales = "free_x") +
    labs(title = "Temperature and Snow Differences Per Day", x = "Difference Type", y = "Value", fill = "Threshold ≥ 5") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(plot)  # Show plot
  dev.off()
}
