import os
import sys
import json
import subprocess


data_dir = "/workspace/LLaMA-Factory/data"
os.makedirs(data_dir, exist_ok=True)

# 3. Define the registration info
dataset_info = {
    "GenerationTag_Alpaca": {
        "file_name": "GenerationTag_Alpaca.json",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output"
        }
    }
}

dataset_info_path = os.path.join(data_dir, "dataset_info.json")
with open(dataset_info_path, "w", encoding="utf-8") as f:
    json.dump(dataset_info, f, indent=2)

print(f"Dataset and registration info saved to {data_dir}.")
print("You can now proceed to the fine-tuning cell.")


import os
import sys
import json
import torch

# 1. Setup paths
llm_path = "/content/LLaMA-Factory"
src_path = os.path.join(llm_path, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 2. Define training configuration
train_args = {
  "stage": "sft",
  "do_train": True,
  "model_name_or_path": "Qwen/Qwen3.5-9B",
  "dataset": "GenerationTag_Alpaca",
  "dataset_dir": "/workspace/LLaMA-Factory/data",
  "template": "qwen3_5_nothink",
  "finetuning_type": "lora",
  "lora_target": "all",
  "output_dir": "qwen_lora_checkpoint",
  "overwrite_output_dir": True,

  # --- CRITICAL MEMORY FIXES ---
  "per_device_train_batch_size": 4, 
  "gradient_accumulation_steps": 4, 
  "gradient_checkpointing": True,    
  "cutoff_len": 16384,                # Reduced from 16384 to prevent OOM
  # -----------------------------

  "lr_scheduler_type": "cosine",
  "logging_steps": 500,
  "save_steps": 1000,
  "learning_rate": 2e-4,
  "num_train_epochs": 2.0,
  "plot_loss": True,
  "fp16": True,
}

try:
    # 3. Import and run using the API
    from llamafactory.train.tuner import run_exp
    print("Successfully imported llamafactory engine.")
    print("Starting fine-tuning...")
    run_exp(train_args)
    print("\nTraining completed successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()