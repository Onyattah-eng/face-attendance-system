import csv
import os
from datetime import datetime

FILE_PATH = "logs/attendance.csv"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # If file doesn't exist, create it
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name", "Date", "Time"])

        # Prevent duplicate entries in same session
        existing_entries = []

        if file_exists:
            with open(FILE_PATH, "r") as r:
                reader = csv.reader(r)
                existing_entries = list(reader)

        for row in existing_entries:
            if row and row[0] == name and row[1] == date:
                return  # already marked today

        writer.writerow([name, date, time])
        print(f"Attendance marked for {name}")