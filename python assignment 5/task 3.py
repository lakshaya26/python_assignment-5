
import time
import sqlite3

# Generate sample data
data = []

stations = ["Adyar", "Guindy", "Velachery"]

for station in stations:
    for day in range(1, 31):
        for hour in range(24):
            pm25 = (day + hour) % 150
            data.append((station, pm25))

print("TOTAL RECORDS:", len(data))

# Method 1: Python loops
start = time.time()

totals = {}
counts = {}

for station, pm25 in data:
    if station not in totals:
        totals[station] = 0
        counts[station] = 0

    totals[station] += pm25
    counts[station] += 1

print("\nPYTHON LOOP RESULTS")

for station in totals:
    average = totals[station] / counts[station]
    print(station, round(average, 2))

loop_time = time.time() - start

# Method 2: SQLite
con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    pm25 REAL
)
""")

con.executemany(
    "INSERT INTO readings VALUES (?, ?)",
    data
)

con.commit()

start = time.time()

result = con.execute("""
SELECT station, AVG(pm25)
FROM readings
GROUP BY station
""")

print("\nSQL RESULTS")

for row in result:
    print(row[0], round(row[1], 2))

sql_time = time.time() - start

# Display execution times
print("\nPERFORMANCE COMPARISON")

print("Python loop time:", round(loop_time, 6), "seconds")
print("SQL query time:", round(sql_time, 6), "seconds")

# Profiling
print("\nPROGRAM PROFILING")

import cProfile

def calculate():
    total = 0

    for station, pm25 in data:
        total += pm25

    return total

cProfile.run("calculate()")

con.close()
