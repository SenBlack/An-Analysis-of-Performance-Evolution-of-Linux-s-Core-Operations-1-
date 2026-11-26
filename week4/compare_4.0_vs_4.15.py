import csv

def read_kbest(csv_path):
    res = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            name = row[0].strip()
            val = row[1].strip()
            if "kbest" in name.lower() and len(row)>=3:
                op = name.replace("kbest","").strip()
                try:
                    res[op] = float(row[2])
                except:
                    pass
    return res

base = read_kbest("raw_csv/output.4.0.5-040005-generic_run1.csv")
test = read_kbest("raw_csv/output.4.15.0-112-generic_run1.csv")

print("| test | v4.0.5 kbest (s) | v4.15 kbest (s) | ratio (v4.15 / v4.0) |")
print("| ---- | ---- | ---- | ---- |")
for op in base:
    if op in test:
        r = test[op] / base[op]
        print(f"| {op} | {base[op]:.10f} | {test[op]:.10f} | {r:.3f} |")
