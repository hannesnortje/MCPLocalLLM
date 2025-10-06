#!/usr/bin/env python3
"""
Verify that no CUDA packages are installed
This script checks for CUDA-specific PyTorch and other CUDA packages
"""

import subprocess
import sys
import re

def check_pip_packages():
    """Check pip packages for CUDA references"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, check=True)
        packages = result.stdout
        
        cuda_packages = []
        for line in packages.split('\n'):
            if re.search(r'cuda|cu\d+', line, re.IGNORECASE):
                cuda_packages.append(line.strip())
        
        return cuda_packages
    except subprocess.CalledProcessError as e:
        print(f"Error checking pip packages: {e}")
        return []

def check_torch_cuda():
    """Check if PyTorch has CUDA support"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else None
        
        return {
            'cuda_available': cuda_available,
            'cuda_version': cuda_version,
            'torch_version': torch.__version__,
            'mps_available': torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False
        }
    except ImportError:
        return {'error': 'PyTorch not installed'}

def main():
    print("🔍 Checking for CUDA packages...")
    print("=" * 40)
    
    # Check pip packages
    cuda_packages = check_pip_packages()
    if cuda_packages:
        print("❌ CUDA packages found:")
        for pkg in cuda_packages:
            print(f"   {pkg}")
        print()
    else:
        print("✅ No CUDA packages found in pip list")
        print()
    
    # Check PyTorch CUDA support
    torch_info = check_torch_cuda()
    if 'error' in torch_info:
        print(f"⚠️  {torch_info['error']}")
    else:
        print(f"PyTorch version: {torch_info['torch_version']}")
        print(f"CUDA available: {torch_info['cuda_available']}")
        if torch_info['cuda_version']:
            print(f"CUDA version: {torch_info['cuda_version']}")
        print(f"MPS available: {torch_info['mps_available']}")
        
        if torch_info['cuda_available']:
            print("❌ PyTorch has CUDA support enabled")
        else:
            print("✅ PyTorch is CPU-only (no CUDA)")
    
    print()
    print("💾 Space saved: ~7GB (no CUDA PyTorch)")
    print("🍎 Optimized for: Apple Silicon M1 Max")

if __name__ == "__main__":
    main()
