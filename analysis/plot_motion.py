import csv
import matplotlib.pyplot as plt

timestamps = []
accel_x = []
accel_y = []
accel_z = []

with open("../data/sample_data.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        timestamps.append(float(row["time"]))
        accel_x.append(float(row["ax"]))
        accel_y.append(float(row["ay"]))
        accel_z.append(float(row["az"]))

plt.plot(timestamps, accel_x, label="X")
plt.plot(timestamps, accel_y, label="Y")
plt.plot(timestamps, accel_z, label="Z")

plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration")
plt.title("StrideSense IMU Motion Data")
plt.legend()

plt.show()