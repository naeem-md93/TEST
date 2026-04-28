#!/usr/bin/env bash
set -e

# 1. Install LLaMA-Factory correctly
cd "$HOME"
rm -rf "$HOME/LLaMA-Factory/"
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory 
pip install .[metrics,bitsandbytes,peft]
pip install accelerate modelscope hf_transfer

# Switch back to content directory
cd "$HOME"
pip install bitsandbytes
pip install transformers==5.2.0
cp ./GenerationTag_Alpaca.json


python main.py
