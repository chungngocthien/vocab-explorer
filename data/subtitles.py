import csv
import math

def to_zipf(freq):
    if not freq or float(freq) == 0:
        return ""
    return round(math.log10(float(freq) * 1_000_000) + 3, 2)

with open("subtitles_10k.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("subtitles_10k.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["rank", "word", "count", "frequency", "zipf"])
    writer.writeheader()
    for row in rows:
        row["zipf"] = to_zipf(row["frequency"])
        writer.writerow(row)

print("Done")