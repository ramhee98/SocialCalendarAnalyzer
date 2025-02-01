import pandas as pd
import re
from datetime import datetime
import timeit

def extract_field(line, pattern):
    """Extracts the first match of a pattern in a line, safely handling missing matches."""
    match = re.search(pattern, line)
    return match.group() if match else None

def analyze_icalendar(file_path):
    # Read the .ics file
    with open(file_path, "r", encoding="utf-8") as file:
        ics_data = file.readlines()
    
    # Extract DTSTART, DTEND, and SUMMARY fields safely
    start_times = [extract_field(line, r"\d{8}T\d{6}") for line in ics_data if line.startswith("DTSTART")]
    end_times = [extract_field(line, r"\d{8}T\d{6}") for line in ics_data if line.startswith("DTEND")]
    summaries = [line.replace("SUMMARY:", "").strip() for line in ics_data if line.startswith("SUMMARY")]

    # Remove None values that indicate parsing issues
    start_times = [s for s in start_times if s]
    end_times = [e for e in end_times if e]

    # Ensure lengths match
    min_length = min(len(start_times), len(end_times), len(summaries))
    start_times, end_times, summaries = start_times[:min_length], end_times[:min_length], summaries[:min_length]

    # Convert times to datetime objects
    start_times = [datetime.strptime(time, "%Y%m%dT%H%M%S") for time in start_times]
    end_times = [datetime.strptime(time, "%Y%m%dT%H%M%S") for time in end_times]

    # Create DataFrame
    calendar_df = pd.DataFrame({
        "Start": start_times,
        "End": end_times,
        "Summary": summaries
    })

    # Compute event durations in minutes
    calendar_df["Duration"] = (calendar_df["End"] - calendar_df["Start"]).dt.total_seconds() / 60

    # Extract names from the Summary field
    def extract_names(summary):
        words = summary.split()
        return [word for word in words if word.lower() not in {"mitm", "und", "bim"}]

    # Expand names into separate rows
    exploded_df = calendar_df.explode("Summary")
    exploded_df["Friends"] = exploded_df["Summary"].apply(extract_names)
    exploded_df = exploded_df.explode("Friends")

    # Aggregate total time per friend
    friend_time_df = exploded_df.groupby("Friends", as_index=False)["Duration"].sum()
    friend_time_df = friend_time_df.sort_values(by="Duration", ascending=False)

    # Save results to CSV
    friend_time_df.to_csv("social_calendar_analysis_python.csv", index=False)
    print("Analysis complete! Results saved as 'social_calendar_analysis_python.csv'.")
    
    # Display results
    print(friend_time_df)

# Example usage
analyze_icalendar("calendar.ics")

# Run benchmark 100 times
#def benchmark():
#    analyze_icalendar("calendar.ics")

#time_taken = timeit.timeit(benchmark, number=100)
#avg_time = time_taken * 1000 / 10
#print(f"Benchmark results: average {avg_time} milliseconds")
