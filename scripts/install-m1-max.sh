#!/bin/bash
# M1 Max Installation Script - No CUDA, M1 Optimized
# This script installs dependencies optimized for Apple M1 Max

set -e

echo "🍎 Installing M1 Max optimized dependencies..."
echo "=============================================="

# Check if running on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "⚠️  Warning: This script is optimized for Apple Silicon (M1/M2/M3)"
    echo "   Current architecture: $(uname -m)"
    echo "   Continuing with CPU-only installation..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install base dependencies (MPS-enabled PyTorch for M1 Max)
echo "📚 Installing base dependencies..."
pip install -e .

# Install MPS-enabled PyTorch for M1 Max (not CPU-only!)
if [[ $(uname -m) == "arm64" ]]; then
    echo "🍎 Installing MPS-enabled PyTorch for Apple Silicon..."
    pip install torch torchvision torchaudio
else
    echo "⚠️  Installing CPU-only PyTorch for non-Apple Silicon..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Install M1 Max training dependencies
echo "🚀 Installing M1 Max training dependencies..."
pip install -e ".[training]"

# Verify installation
echo "✅ Verifying installation..."
python3 -c "
import torch
import sys
print(f'Python: {sys.version}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'MPS available: {torch.backends.mps.is_available() if hasattr(torch.backends, \"mps\") else False}')
print(f'Device count: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')
"

# Install MLX-LM (Apple Silicon only)
if [[ $(uname -m) == "arm64" ]]; then
    echo "🍎 Installing MLX-LM (Apple's native framework)..."
    pip install mlx-lm
    
    echo "🍎 Checking MLX-LM installation..."
    python3 -c "
try:
    import mlx.core as mx
    print(f'MLX available: {mx.is_available()}')
    print(f'MLX devices: {mx.devices()}')
except ImportError:
    print('MLX-LM installation failed')
"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate environment: source venv/bin/activate"
echo "   2. Start Sprint 4 planning on M1 Max"
echo ""
echo "💾 Space saved: ~7GB (no CUDA PyTorch)"
echo "⚡ Performance: MPS + MLX-LM optimized for M1 Max unified memory"
echo "🎯 Training: MLX-LM (primary) + PyTorch MPS (fallback)"
