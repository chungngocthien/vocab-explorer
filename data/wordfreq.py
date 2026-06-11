from wordfreq import top_n_list, word_frequency, zipf_frequency
import csv

words = top_n_list("en", 10000)

with open("wordfreq_10k.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "word", "frequency", "zipf"])
    for i, w in enumerate(words, 1):
        writer.writerow([i, w, word_frequency(w, "en"), zipf_frequency(w, "en")])

print("Done")