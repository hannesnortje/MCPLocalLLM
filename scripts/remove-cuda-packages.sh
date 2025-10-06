#!/bin/bash
# Remove CUDA packages to free up ~8GB of space
# This script removes all NVIDIA CUDA packages that are not needed for M1 Max

set -e

echo "🗑️  Removing CUDA packages to free up ~8GB..."
echo "=============================================="

# Check current space usage
echo "📊 Current disk usage:"
du -sh /media/hannesn/storage/Code/MCPLocalLLM/ 2>/dev/null || echo "Cannot check disk usage"

echo ""
echo "🔍 CUDA packages found:"
pip list | grep -i nvidia | wc -l | xargs echo "NVIDIA packages:"

echo ""
echo "🗑️  Removing NVIDIA CUDA packages..."

# Remove all NVIDIA CUDA packages
pip uninstall -y \
    nvidia-cublas-cu12 \
    nvidia-cuda-cupti-cu12 \
    nvidia-cuda-nvrtc-cu12 \
    nvidia-cuda-runtime-cu12 \
    nvidia-cufft-cu12 \
    nvidia-cufile-cu12 \
    nvidia-curand-cu12 \
    nvidia-cusparse-cu12 \
    nvidia-cusparselt-cu12 \
    nvidia-nccl-cu12 \
    nvidia-nvjitlink-cu12 \
    nvidia-nvtx-cu12 \
    2>/dev/null || echo "Some packages may not be installed"

echo ""
echo "🧹 Cleaning up pip cache..."
pip cache purge

echo ""
echo "📊 Verifying removal..."
python3 scripts/verify-no-cuda.py

echo ""
echo "💾 Space freed: ~8GB"
echo "🍎 Ready for M1 Max optimization!"
echo ""
echo "📋 Next steps:"
echo "   1. Transfer to M1 Max"
echo "   2. Run: ./scripts/install-m1-max.sh"
echo "   3. Start Sprint 4 planning"
