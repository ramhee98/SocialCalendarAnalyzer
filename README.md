# 📅 SocialCalendarAnalyzer

## 📌 Project Overview
**SocialCalendarAnalyzer** is a Python / R-based tool that processes `.ics` (iCalendar) files to extract and analyze event durations. It helps users track time spent with different individuals and export the data to a CSV file for further analysis.

## 🚀 Features
- Parses `.ics` calendar files
- Extracts event start and end times
- Calculates total time spent per person
- Supports both **Python** and **R** implementations
- Outputs results as a structured **CSV file**

## 🛠️ Installation
### **Python Setup**
1. Clone the repository:
   ```sh
   git clone https://github.com/ramhee98/SocialCalendarAnalyzer
   cd ics-event-analyzer
   ```
2. Install dependencies:
   ```sh
   pip install -r pandas
   ```
3. Run the script:
   ```sh
   python social_calendar_analyzer.py
   ```

### **R Setup**
1. Ensure you have R installed.
2. Install required packages in R:
   ```r
   install.packages(c("lubridate", "dplyr", "stringr", "tidyr"))
   ```
3. Optionally install microbenchmark if you want to becnhmark the script
   ```r
   install.packages(c("microbenchmark"))
   ```
4. Run the script in R:
   ```r
   source("social_calendar_analyzer.R")
   analyze_icalendar("calendar.ics")
   ```

## 📊 Output
After running the script, the tool generates a CSV file containing the total time spent with each person. Example output:

| Friends  | Total Time (Minutes) |
|----------|----------------------|
| Person2  | 3240                 |
| Person1  | 1440                 |
| Person3  | 960                  |

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---
🌟 *If you find this project useful, give it a ⭐ on GitHub!*

