import csv
from wordfreq import word_frequency, zipf_frequency
from collections import defaultdict

with open("oxford_raw.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Gộp các POS của cùng một từ
grouped = defaultdict(list)
cefr_map = {}
for r in rows:
    word = r["headword"].strip().lower()
    grouped[word].append(r["pos"].strip())
    cefr_map[word] = r["CEFR"].strip()

enriched = []
for word, pos_list in grouped.items():
    pos_merged = ", ".join(sorted(set(pos_list)))
    enriched.append({
        "word": word,
        "pos": pos_merged,
        "cefr": cefr_map[word],
        "frequency": word_frequency(word, "en"),
        "zipf": zipf_frequency(word, "en"),
    })

enriched.sort(key=lambda x: x["frequency"], reverse=True)

with open("oxford_enriched.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["rank", "word", "pos", "cefr", "frequency", "zipf"])
    writer.writeheader()
    for i, row in enumerate(enriched, 1):
        writer.writerow({**row, "rank": i})

print(f"Done: {len(enriched)} unique words")