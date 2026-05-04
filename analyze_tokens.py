import json
from transformers import AutoTokenizer

# Load the Qwen3.5 / Qwen2.5 tokenizer (same vocabulary)
_TOKENIZER_ID = "Qwen/Qwen2.5-7B"
print(f"Loading tokenizer: {_TOKENIZER_ID} ...")
_tokenizer = AutoTokenizer.from_pretrained(_TOKENIZER_ID, trust_remote_code=True)
print("Tokenizer loaded.\n")

def exact_token_count(text: str) -> int:
    return len(_tokenizer.encode(text, add_special_tokens=False))

def load_data(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze(data, threshold=8000):
    token_counts = []
    over_threshold = []

    for i, sample in enumerate(data):
        instruction = sample.get("instruction", "")
        input_text = sample.get("input", "")
        full_input = instruction + " " + input_text
        count = exact_token_count(full_input)
        token_counts.append(count)
        if count > threshold:
            over_threshold.append((i, count))

    return token_counts, over_threshold

def print_distribution(token_counts, threshold=8000):
    total = len(token_counts)
    buckets = [
        (0, 512),
        (512, 1024),
        (1024, 2048),
        (2048, 4096),
        (4096, 8000),
        (8000, 16000),
        (16000, float("inf")),
    ]

    print(f"{'='*50}")
    print(f"Total samples: {total}")
    print(f"Min tokens:    {min(token_counts)}")
    print(f"Max tokens:    {max(token_counts)}")
    print(f"Mean tokens:   {sum(token_counts)/total:.1f}")
    print(f"{'='*50}")
    print(f"\nToken distribution (exact, Qwen tokenizer):\n")
    print(f"{'Range':<20} {'Count':>8} {'%':>8}")
    print("-" * 40)
    for lo, hi in buckets:
        label = f"{lo}-{hi}" if hi != float("inf") else f"{lo}+"
        count = sum(1 for t in token_counts if lo < t <= hi)
        pct = count / total * 100
        bar = "#" * int(pct / 2)
        print(f"{label:<20} {count:>8} {pct:>7.1f}%  {bar}")

    over = sum(1 for t in token_counts if t > threshold)
    print(f"\n{'='*50}")
    print(f"Samples > {threshold} tokens: {over} ({over/total*100:.1f}%)")
    print(f"{'='*50}")

def save_filtered(data, token_counts, threshold, output_path):
    filtered = [s for s, t in zip(data, token_counts) if t <= threshold]
    removed = len(data) - len(filtered)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(filtered)} samples (removed {removed}) to:\n  {output_path}")

if __name__ == "__main__":
    import sys

    data_path = "/home/parstech6/PArschat_Project/Banket/FineTune/TEST/final.json"
    threshold = 8000

    data = load_data(data_path)
    token_counts, over_threshold = analyze(data, threshold)
    print_distribution(token_counts, threshold)

    # Optionally show indices of long samples
    if over_threshold:
        print(f"\nTop 10 longest samples (index, approx tokens):")
        for idx, cnt in sorted(over_threshold, key=lambda x: -x[1])[:10]:
            print(f"  index={idx:5d}  tokens≈{cnt}")

    # Uncomment to save filtered version (samples <= 8000 tokens):
    save_filtered(data, token_counts, threshold,
                  "/home/parstech6/PArschat_Project/Banket/FineTune/TEST/final_filtered.json")
