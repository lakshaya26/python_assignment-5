
import csv
import io
import sqlite3

# Sample database
con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    pm25 REAL
)
""")

data = [
    ("Adyar", 48),
    ("Adyar", 60),
    ("Guindy", 95),
    ("Guindy", 121)
]

# Insert records
con.executemany(
    "INSERT INTO readings VALUES (?, ?)",
    data
)

con.commit()

# Function to find station average
def station_average(name):
    result = con.execute(
        "SELECT AVG(pm25) FROM readings WHERE station = ?",
        (name,)
    )

    return result.fetchone()[0]


print("STATION AVERAGES")

print("Adyar:", station_average("Adyar"))
print("Guindy:", station_average("Guindy"))

# SQL injection test
print("\nSQL INJECTION TEST")

name = "Adyar' OR '1'='1"

print("Unsafe query result:")

unsafe_query = (
    "SELECT * FROM readings WHERE station = '" + name + "'"
)

print(con.execute(unsafe_query).fetchall())

print("\nSafe query result:")
print(station_average(name))

# Data error testing
print("\nDATA ERROR TESTING")

samples = [
    "station,pm25\nAdyar,48",
    "station;pm25\nAdyar;48",
    "",
    "station,pm25\nAdyar,NA",
    "station,date"
]

for sample in samples:
    try:
        reader = csv.DictReader(io.StringIO(sample))

        if not sample.strip():
            print("Empty data found")
            continue

        if reader.fieldnames != ["station", "pm25"]:
            print("Invalid columns or delimiter")
            continue

        rows = list(reader)

        if not rows:
            print("No records found")
        else:
            print("Valid data:", rows)

    except Exception as error:
        print("Error:", error)

# Simple sentiment checking
print("\nSENTIMENT TEST")

def sentiment(text):
    positive = ["good", "clean", "helpful"]
    negative = ["bad", "dirty", "smoke"]

    score = 0

    for word in text.lower().split():
        if word in positive:
            score += 1
        elif word in negative:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"


print(sentiment("The air is clean and good"))
print(sentiment("The air is bad and dirty"))

con.close()
