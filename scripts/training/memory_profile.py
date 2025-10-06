#!/usr/bin/env python3
"""
Memory Profiling Script for T001-B01
Profiles memory usage for inference and estimates training memory
"""

import gc
import os
import sys

import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_memory_usage():
    """Get current memory usage in GB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024**3)  # Convert to GB


def get_peak_memory():
    """Get peak memory usage in GB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    # Use rss as fallback if peak_wss is not available
    if hasattr(memory_info, "peak_wss"):
        return memory_info.peak_wss / (1024**3)
    else:
        return memory_info.rss / (1024**3)  # Convert to GB


def profile_inference_memory():
    """Profile memory usage during inference"""
    print("=" * 60)
    print("T001-B01: Memory Profiling - Inference")
    print("=" * 60)

    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    print(f"Model: {model_name}")
    print("Framework: axolotl/transformers")
    print()

    # Baseline memory
    baseline_memory = get_memory_usage()
    print(f"Baseline memory: {baseline_memory:.2f} GB")

    try:
        # Load tokenizer
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        tokenizer_memory = get_memory_usage()
        print(
            f"Memory after tokenizer: {tokenizer_memory:.2f} GB "
            f"(+{tokenizer_memory - baseline_memory:.2f} GB)"
        )

        # Load model
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="cpu",
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        model_memory = get_memory_usage()
        print(
            f"Memory after model: {model_memory:.2f} GB (+{model_memory - baseline_memory:.2f} GB)"
        )

        # Run inference
        print("Running inference...")
        prompt = "Write a Python function to calculate Fibonacci sequence"
        inputs = tokenizer.encode(prompt, return_tensors="pt")

        # Measure memory during inference
        gc.collect()  # Clean up before measurement
        pre_inference_memory = get_memory_usage()

        with torch.no_grad():
            model.generate(
                inputs,
                max_new_tokens=50,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        post_inference_memory = get_memory_usage()
        peak_memory = get_peak_memory()

        print(f"Memory before inference: {pre_inference_memory:.2f} GB")
        print(f"Memory after inference: {post_inference_memory:.2f} GB")
        print(f"Peak memory: {peak_memory:.2f} GB")

        # Calculate inference memory usage
        inference_memory = model_memory - baseline_memory
        peak_inference_memory = peak_memory - baseline_memory

        print("\nInference Memory Summary:")
        print(f"Model loading: {inference_memory:.2f} GB")
        print(f"Peak during inference: {peak_inference_memory:.2f} GB")

        return inference_memory, peak_inference_memory, model, tokenizer

    except Exception as e:
        print(f"✗ Error during inference profiling: {e}")
        return 0, 0, None, None


def estimate_training_memory(model, tokenizer):
    """Estimate memory usage for QLoRA training"""
    print("\n" + "=" * 60)
    print("T001-B01: Memory Profiling - Training Estimate")
    print("=" * 60)

    print("Estimating QLoRA training memory requirements...")
    print("Configuration: LoRA rank=16, alpha=32, 4-bit quantization, batch_size=1")
    print()

    try:
        # Get model parameters
        total_params = sum(p.numel() for p in model.parameters())
        print(f"Total model parameters: {total_params:,} ({total_params/1e9:.2f}B)")

        # Estimate LoRA parameters (assuming we train all linear layers)
        # For Qwen2.5-7B, typical LoRA target modules:
        # q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
        # Each has shape [hidden_size, hidden_size] = [3584, 3584]
        hidden_size = model.config.hidden_size  # 3584
        lora_rank = 16
        lora_alpha = 32

        # Estimate LoRA parameters per layer
        # LoRA adds: rank * (input_dim + output_dim) parameters per matrix
        # For each attention layer: 4 matrices (q, k, v, o)
        # For each MLP layer: 3 matrices (gate, up, down)
        attention_layers = model.config.num_hidden_layers  # 28
        mlp_layers = model.config.num_hidden_layers  # 28

        # Attention LoRA params: 4 matrices * rank * (hidden_size + hidden_size) * num_layers
        attention_lora_params = 4 * lora_rank * (hidden_size + hidden_size) * attention_layers

        # MLP LoRA params: 3 matrices * rank * (hidden_size + hidden_size) * num_layers
        mlp_lora_params = 3 * lora_rank * (hidden_size + hidden_size) * mlp_layers

        total_lora_params = attention_lora_params + mlp_lora_params

        print(f"LoRA rank: {lora_rank}")
        print(f"LoRA alpha: {lora_alpha}")
        print(f"Hidden size: {hidden_size}")
        print(f"Number of layers: {attention_layers}")
        print(f"Estimated LoRA parameters: {total_lora_params:,} ({total_lora_params/1e6:.2f}M)")

        # Memory estimation (rough calculations)
        # Base model: ~14GB (from our measurement)
        # LoRA parameters: ~50MB (16-bit)
        # Gradients: ~50MB (16-bit)
        # Optimizer states: ~100MB (AdamW)
        # Activations: ~2-4GB (depends on sequence length)
        # Overhead: ~1-2GB (PyTorch, CUDA, etc.)

        base_model_memory = 14.0  # GB (measured)
        lora_params_memory = total_lora_params * 2 / (1024**3)  # 16-bit = 2 bytes
        gradients_memory = total_lora_params * 2 / (1024**3)  # 16-bit = 2 bytes
        optimizer_memory = total_lora_params * 4 / (1024**3)  # AdamW = 4 bytes per param
        activations_memory = 3.0  # GB (estimated for sequence length ~2048)
        overhead_memory = 1.5  # GB (PyTorch overhead)

        total_training_memory = (
            base_model_memory
            + lora_params_memory
            + gradients_memory
            + optimizer_memory
            + activations_memory
            + overhead_memory
        )

        print("\nMemory Breakdown (QLoRA Training):")
        print(f"Base model: {base_model_memory:.2f} GB")
        print(f"LoRA parameters: {lora_params_memory:.3f} GB")
        print(f"Gradients: {gradients_memory:.3f} GB")
        print(f"Optimizer states: {optimizer_memory:.3f} GB")
        print(f"Activations: {activations_memory:.2f} GB")
        print(f"Overhead: {overhead_memory:.2f} GB")
        print(f"Total estimated: {total_training_memory:.2f} GB")

        # Check against 16GB target
        target_memory = 16.0
        headroom = target_memory - total_training_memory

        print("\nMemory Target Analysis:")
        print(f"Target: {target_memory:.2f} GB")
        print(f"Estimated: {total_training_memory:.2f} GB")
        print(f"Headroom: {headroom:.2f} GB")

        if total_training_memory <= target_memory:
            print("✓ Training memory within target (≤16GB)")
            status = "PASS"
        else:
            print("✗ Training memory exceeds target (>16GB)")
            status = "FAIL"

        return total_training_memory, headroom, status

    except Exception as e:
        print(f"✗ Error during training estimation: {e}")
        return 0, 0, "ERROR"


def main():
    """Main function"""
    print("Starting Qwen2.5-Coder-7B-Instruct memory profiling...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()

    # Profile inference memory
    inference_memory, peak_memory, model, tokenizer = profile_inference_memory()

    if model is None:
        print("\n✗ Memory profiling failed - could not load model")
        return 1

    # Estimate training memory
    training_memory, headroom, status = estimate_training_memory(model, tokenizer)

    # Final summary
    print("\n" + "=" * 60)
    print("T001-B01: Memory Profiling Summary")
    print("=" * 60)
    print("Model: Qwen2.5-Coder-7B-Instruct")
    print("Framework: axolotl/transformers")
    print()
    print(f"Inference Memory: {inference_memory:.2f} GB")
    print(f"Peak Inference Memory: {peak_memory:.2f} GB")
    print(f"Training Memory (est): {training_memory:.2f} GB")
    print(f"Headroom from 16GB: {headroom:.2f} GB")
    print(f"Training Status: {status}")
    print()

    if status == "PASS":
        print("✓ Memory profiling completed successfully")
        print("✓ Training memory within 16GB target")
        return 0
    else:
        print("✗ Memory profiling issues detected")
        print("✗ Training memory may exceed 16GB target")
        return 1


if __name__ == "__main__":
    sys.exit(main())
