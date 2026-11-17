
import sqlite3
import time

# Sentiment words
POSITIVE = {
    "good", "clean", "fast", "helpful", "improved"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke", "broken"
}

NEGATORS = {"not", "never", "no"}

# Sentiment function
def sentiment(text):
    words = text.lower().replace(".", "").replace(",", "").split()

    score = 0

    for i, word in enumerate(words):
        value = 0

        if word in POSITIVE:
            value = 1

        elif word in NEGATIVE:
            value = -1

        if i > 0 and words[i - 1] in NEGATORS:
            value = -value

        score += value

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    else:
        return "Neutral"


# Sample complaints
complaints = [
    "The air is good",
    "The area is dirty",
    "The service is helpful",
    "Smoke from the factory",
    "The road is clean",
    "The service is slow",
    "Not bad, service improved",
    "The staff were not helpful",
    "The air quality is good",
    "The pollution is bad"
]

# Create 50 complaints
all_complaints = complaints * 5

print("TOTAL COMPLAINTS:", len(all_complaints))

# Analyse complaints
positive = 0
negative = 0
neutral = 0

print("\nCOMPLAINT ANALYSIS")

for complaint in all_complaints:
    result = sentiment(complaint)

    print(complaint, ":", result)

    if result == "Positive":
        positive += 1

    elif result == "Negative":
        negative += 1

    else:
        neutral += 1

# Display summary
print("\nCOMPLAINT SUMMARY")

print("Positive:", positive)
print("Negative:", negative)
print("Neutral:", neutral)

# Simple summary
print("\nOVERALL SUMMARY")

if negative > positive:
    print("Most complaints report pollution or service problems.")

elif positive > negative:
    print("Most complaints contain positive feedback.")

else:
    print("Positive and negative complaints are balanced.")


# SQLite database
con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

data = []

for i in range(10000):
    station = "Station" + str(i % 10)
    day = "2026-10-" + str((i % 30) + 1)
    pm25 = i % 150

    data.append((station, day, pm25))

con.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    data
)

con.commit()

# Query before index
start = time.time()

for i in range(100):
    con.execute("""
        SELECT AVG(pm25)
        FROM readings
        WHERE station = ? AND day = ?
    """, ("Station1", "2026-10-10")).fetchone()

before = time.time() - start

# Create index
con.execute("""
CREATE INDEX station_day_index
ON readings(station, day)
""")

# Query after index
start = time.time()

for i in range(100):
    con.execute("""
        SELECT AVG(pm25)
        FROM readings
        WHERE station = ? AND day = ?
    """, ("Station1", "2026-10-10")).fetchone()

after = time.time() - start

print("\nINDEX PERFORMANCE")

print("Before index:", round(before, 6), "seconds")
print("After index:", round(after, 6), "seconds")

con.close()
