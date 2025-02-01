
import pandas as pd
import re
from datetime import datetime
import timeit

# Function to extract events from .ics file
def parse_icalendar(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    events = []
    event = {}
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("DTSTART"):
            dt_start = re.search(r"\d{8}T\d{6}Z", line)
            if dt_start:
                event["Start"] = datetime.strptime(dt_start.group(), "%Y%m%dT%H%M%SZ")

        if line.startswith("DTEND"):
            dt_end = re.search(r"\d{8}T\d{6}Z", line)
            if dt_end:
                event["End"] = datetime.strptime(dt_end.group(), "%Y%m%dT%H%M%SZ")

        if line.startswith("SUMMARY"):
            event["Summary"] = line.split(":", 1)[1].strip()
        
        if line == "END:VEVENT":
            if "Start" in event and "End" in event and "Summary" in event:
                event["Total_Time_Minutes"] = (event["End"] - event["Start"]).total_seconds() / 60  # Duration in minutes
                events.append(event)
            event = {}

    return pd.DataFrame(events)

# Function to analyze calendar events and compute time spent with each person
def analyze_calendar(file_path, output_path):
    calendar_df = parse_icalendar(file_path)

    # Extract names from the Summary field (assuming names are single words or comma-separated)
    calendar_df["Friends"] = calendar_df["Summary"].apply(lambda x: re.findall(r'\b\w+\b', x))

    # Normalize names by flattening and grouping total time spent with each person
    friends_time = (
        calendar_df.explode("Friends")  # Expand multiple names in the same event
        .groupby("Friends", as_index=False)["Total_Time_Minutes"].sum()
        .sort_values(by="Total_Time_Minutes", ascending=False)
    )

    # Save the results to a CSV file
    friends_time.to_csv(output_path, index=False)
    print(f"Analysis complete! Results saved as '{output_path}'.")

# Example usage
analyze_calendar("calendar.ics", "social_calendar_analysis_python.csv")

# Run benchmark 100 times
#def benchmark():
#    analyze_icalendar("calendar.ics")

#time_taken = timeit.timeit(benchmark, number=100)
#avg_time = time_taken * 1000 / 10
#print(f"Benchmark results: average {avg_time} milliseconds")