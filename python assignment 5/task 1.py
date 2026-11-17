
import csv
import io
import sqlite3

# Sample raw data
RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Adyar,2026-10-04,1200
"""

# Display original data
print("BEFORE CLEANING")
print(RAW)

# Data cleaning function
def load_clean(text):
    rows = []

    reader = csv.DictReader(io.StringIO(text))

    for row in reader:
        value = row["pm25"].strip()

        if value == "" or value.upper() == "NA":
            continue

        pm25 = float(value)

        if pm25 < 0 or pm25 > 999:
            continue

        rows.append((
            row["station"],
            row["date"],
            pm25
        ))

    return rows


# Min-max normalisation
def min_max(values):
    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [0.0 for value in values]

    result = []

    for value in values:
        scaled = (value - minimum) / (maximum - minimum)
        result.append(round(scaled, 3))

    return result


# Clean the data
clean = load_clean(RAW)

print("\nAFTER CLEANING")
print(clean)

# Normalisation
values = [pm for station, date, pm in clean]

print("\nNORMALISED VALUES")
print(min_max(values))


# Store data in SQLite
con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    clean
)

con.commit()

# SQL query 1: Average pollution
print("\nAVERAGE PM2.5")

result = con.execute("""
SELECT station, AVG(pm25)
FROM readings
GROUP BY station
""")

for row in result:
    print(row)

# SQL query 2: Highest reading
print("\nHIGHEST PM2.5")

result = con.execute("""
SELECT station, MAX(pm25)
FROM readings
GROUP BY station
""")

for row in result:
    print(row)

# SQL query 3: All readings
print("\nALL CLEANED READINGS")

result = con.execute("SELECT * FROM readings")

for row in result:
    print(row)

con.close()
