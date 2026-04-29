import json
import os
import requests
import urllib3
import time

urllib3.disable_warnings()

# ------------------------------
CLUSTER_DIR = "/home/Downloads/cluster_samples_QT/"
ES_URL = "https://localhost:9200/parschat_logs/_search"

VERIFY_SSL = False
AUTH = ("elastic", "KdyqA4zcgjB3X3603v")

SAVE_EVERY = 20
REQUEST_SLEEP = 0.05


# ------------------------------
def get_query_tag(trace_id):

    body = {
        "query": {
            "bool": {
                "must": [
                    {"exists": {"field": "chain_calls"}},
                    {"term": {"chain_calls.trace_id": trace_id}}
                ]
            }
        },
        "_source": {
            "excludes": [
                "faqs.question_vector",
                "faqs.answer_vector",
                "data_summaries.vector",
                "child_summaries.vector",
                "chunks.vector",
                "shots.vector"
            ]
        },
        "size": 5
    }

    try:
        response = requests.get(
            ES_URL,
            json=body,
            auth=AUTH,
            verify=VERIFY_SSL,
            timeout=30
        )

        if response.status_code != 200:
            print("❌ ES ERROR:", response.text)
            return None

        data = response.json()
        hits = data.get("hits", {}).get("hits", [])

        for hit in hits:
            chain = hit["_source"].get("chain_calls", {})

            if chain.get("chain_name") == "QueryTag":
                return {
                    "chain_name": chain.get("chain_name"),
                    "output_data": chain.get("output_data"),
                    "input_data": chain.get("input_data")
                }

    except Exception as e:
        print(f"❌ ERROR for trace_id {trace_id}: {e}")

    return None


# ------------------------------
files = [f for f in os.listdir(CLUSTER_DIR) if f.endswith(".json")]

for file_name in files:

    path = os.path.join(CLUSTER_DIR, file_name)
    print(f"\n📂 Processing file → {file_name}")

    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    total = len(items)
    processed_count = 0
    skipped_count = 0

    for i, item in enumerate(items):

        if "output_data" in item and "input_data" in item:
            skipped_count += 1
            continue

        trace_id = item.get("trace_id")

        if not trace_id:
            continue

        result = get_query_tag(trace_id)

        if result:
            item["output_data"] = result["output_data"]
            item["input_data"] = result["input_data"]
            item["chain_name"] = result["chain_name"]
            processed_count += 1
        else:
            print(f"⚠ No QueryTag found for {trace_id}")

        if i % SAVE_EVERY == 0:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"💾 Auto-saved at record {i}/{total}")

        time.sleep(REQUEST_SLEEP)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ Finished file → {file_name}")
    print(f"   Processed: {processed_count}")
    print(f"   Skipped (already done): {skipped_count}")
    print(f"   Total: {total}")
