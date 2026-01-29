import pandas as pd
import os

# Path to attendance CSV
csv_path = "attendance.csv"  # Make sure this file is in the same folder

# Check if the file exists
if not os.path.exists(csv_path):
    print("⚠️ Attendance file not found. No attendance to display.")
else:
    # Read the CSV
    df = pd.read_csv(csv_path, encoding="utf-8")

    if df.empty:
        print("⚠️ Attendance sheet is empty.")
    else:
        # Print the attendance sheet nicely
        print("\n📋 Complete Attendance Sheet:\n")
        print(df.to_string(index=False))
