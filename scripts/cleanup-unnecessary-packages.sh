#!/bin/bash
# Remove unnecessary packages to free up space for M1 Max
# This script removes packages not needed for M1 Max training

set -e

echo "🧹 Cleaning up unnecessary packages for M1 Max..."
echo "================================================"

# Check current space
echo "📊 Current virtual environment size:"
du -sh .venv/

echo ""
echo "🗑️  Removing unnecessary packages..."

# Remove packages not needed for M1 Max training
source .venv/bin/activate

# Remove UI packages (not needed for training)
pip uninstall -y gradio gradio_client

# Remove quantization packages (not available on Apple Silicon)
pip uninstall -y bitsandbytes

# Remove cloud packages (not needed for local training)
pip uninstall -y oci ocifs

# Remove data science packages (not needed for basic training)
pip uninstall -y pandas scipy scikit-learn

# Remove monitoring packages (not needed for basic training)
pip uninstall -y wandb

# Remove compiler packages (not needed for M1 Max)
pip uninstall -y triton llvmlite numba

# Remove Apache Arrow (not needed for basic training)
pip uninstall -y pyarrow

# Remove torchao (PyTorch optimization, not needed for M1 Max)
pip uninstall -y torchao

# Remove xformers (attention optimization, not needed for basic training)
pip uninstall -y xformers

# Remove mistral packages (not needed for Qwen training)
pip uninstall -y mistral_common

echo ""
echo "🧹 Cleaning up pip cache..."
pip cache purge

echo ""
echo "📊 Final virtual environment size:"
du -sh .venv/

echo ""
echo "💾 Space saved by removing unnecessary packages"
echo "🍎 Ready for M1 Max with only essential packages!"
