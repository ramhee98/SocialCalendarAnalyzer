# Install necessary packages if not already installed
# install.packages("lubridate")  # For handling dates
# install.packages("dplyr")      # For data manipulation
# install.packages("stringr")    # For string manipulation
# install.packages("tidyr")      # For handling list columns
# Optional
# install.packages("microbenchmark") # For handling benchmarks
# Load libraries
library(lubridate)
library(dplyr)
library(stringr)
library(tidyr)
#library(microbenchmark)

# Function to analyze time spent with friends
analyze_icalendar <- function(file_path) {
  # Read the .ics file as raw text
  ics_data <- readLines(file_path, encoding = "UTF-8")
  
  # Extract DTSTART, DTEND, and SUMMARY fields
  start_times <- str_extract(ics_data[str_detect(ics_data, "^DTSTART")], "\\d{8}T\\d{6}Z")
  end_times <- str_extract(ics_data[str_detect(ics_data, "^DTEND")], "\\d{8}T\\d{6}Z")
  summaries <- str_remove(ics_data[str_detect(ics_data, "^SUMMARY")], "^SUMMARY:")
  
  # Ensure lengths match
  min_length <- min(length(start_times), length(end_times), length(summaries))
  start_times <- start_times[1:min_length]
  end_times <- end_times[1:min_length]
  summaries <- summaries[1:min_length]
  
  # Convert to dataframe
  calendar_df <- data.frame(
    Start = ymd_hms(start_times, tz = "UTC"),
    End = ymd_hms(end_times, tz = "UTC"),
    Summary = summaries,
    stringsAsFactors = FALSE
  )
  
  # Compute event durations
  calendar_df <- calendar_df %>%
    mutate(Duration = as.numeric(difftime(End, Start, units = "mins")))
  
  # Extract names from the Summary field
  calendar_df <- calendar_df %>%
    mutate(Friends = str_extract_all(Summary, "\\b\\w+\\b")) %>%  # Extract all words as names
    unnest(Friends) %>%
    group_by(Friends) %>%
    summarise(Total_Time_Minutes = sum(Duration, na.rm = TRUE)) %>%
    arrange(desc(Total_Time_Minutes))
  
  # Display results
  print(calendar_df)

  # Save results to CSV
  write.csv(calendar_df, "social_calendar_analysis_r.csv", row.names = FALSE)
  cat("Analysis complete! Results saved as 'social_calendar_analysis_r.csv'.\n")
}

# Example usage
# analyze_icalendar("calendar.ics")

# Run microbenchmark 100 times
# benchmark_results <- microbenchmark(
#   analyze_icalendar("calendar.ics"),
#   times = 100
# )

# Display benchmark results
# print(benchmark_results)
