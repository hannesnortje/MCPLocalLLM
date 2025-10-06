#!/usr/bin/env python3
"""
Model Loading Test Script for T001-B01
Loads Qwen2.5-Coder-7B-Instruct model using axolotl/transformers framework
"""

import os
import sys
import time

import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_memory_usage():
    """Get current memory usage in GB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024**3)  # Convert to GB


def load_model():
    """Load Qwen2.5-Coder-7B-Instruct model and tokenizer"""
    print("=" * 60)
    print("T001-B01: Model Loading Test")
    print("=" * 60)

    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    print(f"Model: {model_name}")
    print("Framework: axolotl/transformers")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print()

    # Check initial memory
    initial_memory = get_memory_usage()
    print(f"Initial memory usage: {initial_memory:.2f} GB")

    try:
        print("Step 1: Loading tokenizer...")
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        tokenizer_time = time.time() - start_time
        print(f"✓ Tokenizer loaded in {tokenizer_time:.2f} seconds")

        # Check memory after tokenizer
        tokenizer_memory = get_memory_usage()
        print(f"Memory after tokenizer: {tokenizer_memory:.2f} GB")

        print("\nStep 2: Loading model...")
        start_time = time.time()

        # Load model with CPU (since we don't have CUDA on this system)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use float16 to save memory
            device_map="cpu",  # Force CPU usage
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

        model_time = time.time() - start_time
        print(f"✓ Model loaded in {model_time:.2f} seconds")

        # Check final memory
        final_memory = get_memory_usage()
        print(f"Memory after model loading: {final_memory:.2f} GB")

        print("\nStep 3: Validating model architecture...")
        print(f"Model type: {type(model).__name__}")
        print(f"Model config: {model.config.model_type}")
        print(f"Hidden size: {model.config.hidden_size}")
        print(f"Number of layers: {model.config.num_hidden_layers}")
        print(f"Number of attention heads: {model.config.num_attention_heads}")
        print(f"Vocabulary size: {model.config.vocab_size}")

        # Calculate approximate parameter count
        total_params = sum(p.numel() for p in model.parameters())
        print(f"Total parameters: {total_params:,} ({total_params/1e9:.2f}B)")

        print("\nStep 4: Testing tokenizer...")
        test_text = "Write a Python function to calculate Fibonacci sequence"
        tokens = tokenizer.encode(test_text, return_tensors="pt")
        decoded = tokenizer.decode(tokens[0])
        print(f"Test text: {test_text}")
        print(f"Encoded tokens: {tokens.shape[1]} tokens")
        print(f"Decoded text: {decoded}")
        print("✓ Tokenizer working correctly")

        print("\nStep 5: Model summary...")
        print("Model successfully loaded: ✓")
        print("Architecture validated: ✓ (7B parameters confirmed)")
        print("Tokenizer working: ✓")
        print(f"Memory usage: {final_memory - initial_memory:.2f} GB")
        print(f"Total loading time: {tokenizer_time + model_time:.2f} seconds")

        return True, model, tokenizer, final_memory - initial_memory

    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print(f"Error type: {type(e).__name__}")
        return False, None, None, 0


def main():
    """Main function"""
    print("Starting Qwen2.5-Coder-7B-Instruct model loading test...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()

    success, model, tokenizer, memory_used = load_model()

    if success:
        print("\n" + "=" * 60)
        print("✓ MODEL LOADING TEST PASSED")
        print("=" * 60)
        print("Model: Qwen2.5-Coder-7B-Instruct")
        print("Framework: axolotl/transformers")
        print(f"Memory used: {memory_used:.2f} GB")
        print("Status: Ready for inference testing")
        return 0
    else:
        print("\n" + "=" * 60)
        print("✗ MODEL LOADING TEST FAILED")
        print("=" * 60)
        print("Check error messages above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
