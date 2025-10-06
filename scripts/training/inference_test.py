#!/usr/bin/env python3
"""
Inference Test Script for T001-B01
Tests basic inference with Qwen2.5-Coder-7B-Instruct model
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


def run_inference():
    """Run basic inference test with the model"""
    print("=" * 60)
    print("T001-B01: Basic Inference Test")
    print("=" * 60)

    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    print(f"Model: {model_name}")
    print("Framework: axolotl/transformers")
    print()

    # Check initial memory
    initial_memory = get_memory_usage()
    print(f"Initial memory usage: {initial_memory:.2f} GB")

    try:
        print("Step 1: Loading model and tokenizer...")
        start_time = time.time()

        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="cpu",
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

        load_time = time.time() - start_time
        print(f"✓ Model loaded in {load_time:.2f} seconds")

        # Check memory after loading
        load_memory = get_memory_usage()
        print(f"Memory after loading: {load_memory:.2f} GB")

        print("\nStep 2: Preparing test prompts...")
        test_prompts = [
            "Write a Python function to calculate Fibonacci sequence",
            "Create a simple HTTP server in Python",
            "Implement a binary search algorithm in Python",
        ]

        print(f"Number of test prompts: {len(test_prompts)}")

        print("\nStep 3: Running inference tests...")
        all_responses = []

        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n--- Test {i}: {prompt[:50]}... ---")

            # Encode input
            inputs = tokenizer.encode(prompt, return_tensors="pt")
            input_length = inputs.shape[1]
            print(f"Input tokens: {input_length}")

            # Run inference
            start_inference = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_new_tokens=100,  # Generate up to 100 new tokens
                    temperature=0.7,  # Moderate creativity
                    do_sample=True,  # Enable sampling
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                )

            inference_time = time.time() - start_inference

            # Decode output
            full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_text = full_response[len(prompt) :].strip()

            # Calculate metrics
            total_tokens = outputs.shape[1]
            new_tokens = total_tokens - input_length
            tokens_per_second = new_tokens / inference_time if inference_time > 0 else 0

            print(f"Generated tokens: {new_tokens}")
            print(f"Inference time: {inference_time:.2f} seconds")
            print(f"Speed: {tokens_per_second:.2f} tokens/sec")
            print(f"Response length: {len(generated_text)} characters")

            # Check response quality
            is_coherent = len(generated_text) > 20 and not generated_text.startswith("I don't know")
            print(f"Response coherent: {'✓' if is_coherent else '✗'}")

            # Store response
            response_data = {
                "prompt": prompt,
                "response": generated_text,
                "tokens": new_tokens,
                "time": inference_time,
                "speed": tokens_per_second,
                "coherent": is_coherent,
            }
            all_responses.append(response_data)

            print(f"Response preview: {generated_text[:100]}...")

        print("\nStep 4: Analyzing results...")

        # Calculate aggregate metrics
        total_tokens = sum(r["tokens"] for r in all_responses)
        total_time = sum(r["time"] for r in all_responses)
        avg_speed = total_tokens / total_time if total_time > 0 else 0
        coherent_count = sum(1 for r in all_responses if r["coherent"])

        print(f"Total generated tokens: {total_tokens}")
        print(f"Total inference time: {total_time:.2f} seconds")
        print(f"Average speed: {avg_speed:.2f} tokens/sec")
        print(f"Coherent responses: {coherent_count}/{len(all_responses)}")

        # Check final memory
        final_memory = get_memory_usage()
        print(f"Final memory usage: {final_memory:.2f} GB")

        print("\nStep 5: Test validation...")

        # Validation criteria
        min_tokens = 20  # Minimum tokens per response
        min_speed = 1.0  # Minimum tokens per second
        min_coherent = 2  # Minimum coherent responses out of 3

        tokens_ok = all(r["tokens"] >= min_tokens for r in all_responses)
        speed_ok = avg_speed >= min_speed
        coherent_ok = coherent_count >= min_coherent

        print(f"Token count check: {'✓' if tokens_ok else '✗'} (min {min_tokens} tokens)")
        print(f"Speed check: {'✓' if speed_ok else '✗'} (min {min_speed} tokens/sec)")
        print(f"Coherence check: {'✓' if coherent_ok else '✗'} (min {min_coherent} coherent)")

        all_tests_pass = tokens_ok and speed_ok and coherent_ok

        return all_tests_pass, all_responses, avg_speed, final_memory - initial_memory

    except Exception as e:
        print(f"✗ Error during inference: {e}")
        print(f"Error type: {type(e).__name__}")
        return False, [], 0, 0


def main():
    """Main function"""
    print("Starting Qwen2.5-Coder-7B-Instruct inference test...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()

    success, responses, avg_speed, memory_used = run_inference()

    if success:
        print("\n" + "=" * 60)
        print("✓ INFERENCE TEST PASSED")
        print("=" * 60)
        print("Model: Qwen2.5-Coder-7B-Instruct")
        print("Framework: axolotl/transformers")
        print(f"Average speed: {avg_speed:.2f} tokens/sec")
        print(f"Memory used: {memory_used:.2f} GB")
        print("Status: Ready for memory profiling")
        return 0
    else:
        print("\n" + "=" * 60)
        print("✗ INFERENCE TEST FAILED")
        print("=" * 60)
        print("Check error messages above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
