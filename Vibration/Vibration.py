import csv
import random
from datetime import datetime, timedelta

# Define constants
vehicle_number = "AB123CD"
latitude = 16.65383
longitude = 74.261589
threshold = 500
rows_to_generate = 100

# Generate data function
start_time = datetime.strptime("2024-12-12 00:29:33", "%Y-%m-%d %H:%M:%S")
data = []
for i in range(rows_to_generate):
    vibration_value = random.randint(0, 1000)  # Random vibration value
    timestamp = (start_time + timedelta(seconds=i * 3)).strftime("%Y-%m-%d %H:%M:%S")  # Increment timestamp by 3 seconds
    data.append([vehicle_number, latitude, longitude, vibration_value, timestamp])

# Write to CSV file
output_file = "arduino_output.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Vehicle Number", "Latitude", "Longitude", "Vibration Value", "Timestamp"])
    # Write the data rows
    writer.writerows(data)

print(f"Data has been written to {output_file} with {rows_to_generate} rows.")
