import os
import json

CLUSTER_DIR = "/home/ghamari/Desktop/parschat/parschat-logic/data/final/cluster_samples"   # پوشه‌ای که فایل‌های cluster در آن هستند

removed = 0

for filename in os.listdir(CLUSTER_DIR):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(CLUSTER_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        if "output_data" in item:
            del item["output_data"]
            removed += 1

        if "output" in item:   # اگر قبلاً parse شده باشد
            del item["output"]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Removed {removed} output fields")
