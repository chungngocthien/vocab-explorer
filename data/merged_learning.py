import csv

def learning_score(wf_zipf, sub_zipf):
    if not wf_zipf or not sub_zipf:
        return ""
    wf = float(wf_zipf)
    sub = float(sub_zipf)
    avg = (wf + sub) / 2
    if avg == 0:
        return ""
    return round(abs(wf - sub) / (avg ** 2), 6)

with open("merged.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    row["learning_score"] = learning_score(row["wf_zipf"], row["sub_zipf"])

rows.sort(key=lambda x: float(x["learning_score"]) if x["learning_score"] else 999)

fieldnames = ["learning_rank", "word", "wf_rank", "wf_pct", "wf_zipf",
              "sub_rank", "sub_pct", "sub_zipf", "ox_cefr", "ox_pos", "learning_score"]

with open("merged_learning.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i, row in enumerate(rows, 1):
        row["learning_rank"] = i
        writer.writerow(row)

print("Done")