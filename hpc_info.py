#!/usr/bin/env python3
"""
hpc_info.py - Display HPC configuration and capabilities
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.hpc import get_hpc_config


def main():
    """Display HPC information."""
    print("\n🚀 Initializing HPC Configuration...\n")
    
    # Get HPC config
    hpc_config = get_hpc_config()
    
    # Print configuration
    hpc_config.print_info()
    
    # Show recommendations
    print("\n💡 Recommendations:")
    
    if not hpc_config.has_cuda:
        print("  • Install CUDA for GPU acceleration")
        print("    https://developer.nvidia.com/cuda-downloads")
    
    if not hpc_config.has_rapids:
        print("  • Install RAPIDS for GPU-accelerated data processing")
        print("    https://rapids.ai/start.html")
    
    if not hpc_config.has_numba:
        print("  • Install Numba for JIT compilation")
        print("    pip install numba")
    
    if hpc_config.backend == 'rapids':
        print("  ✅ You have the best performance configuration!")
    elif hpc_config.backend == 'cuda':
        print("  ✅ Good performance with CUDA support")
    else:
        print("  ℹ️  Running on CPU - consider GPU acceleration for large datasets")
    
    # Show optimal settings
    print("\n⚙️  Optimal Settings:")
    ml_params = hpc_config.get_ml_params()
    print(f"  XGBoost tree_method: {ml_params['tree_method']}")
    print(f"  XGBoost predictor: {ml_params['predictor']}")
    
    dask_config = hpc_config.get_dask_config()
    print(f"  Dask scheduler: {dask_config['scheduler']}")
    print(f"  Dask workers: {dask_config['num_workers']}")
    
    # Show batch size recommendations
    print("\n📊 Recommended Batch Sizes:")
    for size in [100, 1000, 10000, 100000]:
        batch_size = hpc_config.optimize_for_batch_size(size)
        print(f"  {size:,} items → batch size: {batch_size:,}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
