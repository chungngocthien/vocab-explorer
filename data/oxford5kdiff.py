import csv

# 1. Tải dữ liệu CEFR-J
cefrj = {}
with open("oxford_raw.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        word = row["headword"].strip().lower()
        cefrj[word] = {
            "cefr": row["CEFR"].strip(),
            "pos": row["pos"].strip()
        }

# 2. Tải dữ liệu Oxford 5k
ox5k = {}
with open("oxford5k_raw.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        word = row["word"].strip().lower()
        level = row["level"].strip().upper()
        pos = row["pos"].strip()
        if word not in ox5k:
            ox5k[word] = {"cefr": level, "pos": pos}
        else:
            ox5k[word]["pos"] += ", " + pos

# 3. Phân loại xung đột thành 2 nhóm riêng biệt
cefr_diff_only = []  # Lệch nhãn CEFR, trùng PoS
pos_diff_only = []   # Lệch PoS (bất kể CEFR)

for word, info_j in cefrj.items():
    if word in ox5k:
        cj = info_j["cefr"]
        c5 = ox5k[word]["cefr"]
        pos_j = info_j["pos"]
        pos_5k = ox5k[word]["pos"]
        
        entry = {
            "word": word,
            "cefrj_cefr": cj,
            "ox5k_cefr": c5,
            "cefrj_pos": pos_j,
            "ox5k_pos": pos_5k
        }
        
        # Nếu lệch PoS -> cho vào nhóm dưới
        if pos_j != pos_5k:
            pos_diff_only.append(entry)
        # Nếu trùng PoS nhưng lại lệch nhãn CEFR -> cho vào nhóm trên
        elif cj != c5:
            cefr_diff_only.append(entry)

# 4. Xuất chung vào một file, ngăn cách bằng "___"
fields = ["word", "cefrj_cefr", "ox5k_cefr", "cefrj_pos", "ox5k_pos"]
filename = "cefr_label_conflicts.csv"

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    
    # Ghi phần 1: Lệch nhãn CEFR
    writer.writeheader()
    writer.writerows(cefr_diff_only)
    
    # Ghi dòng ngăn cách bằng cách viết text thô trực tiếp
    f.write("___\n")
    
    # Ghi phần 2: Lệch PoS (Không kèm header để tránh làm gãy cấu trúc parse thô nếu cần)
    writer.writerows(pos_diff_only)

print(f"Hoàn thành! Nhóm 1 (Lệch CEFR): {len(cefr_diff_only)} từ. Nhóm 2 (Lệch PoS): {len(pos_diff_only)} từ.")