"""
HPC Configuration - Detects and configures high-performance computing resources.
"""
import os
import warnings
from typing import Dict, Any, Optional


class HPCConfig:
    """Configuration for high-performance computing resources."""
    
    def __init__(self):
        """Initialize HPC configuration."""
        self.has_cuda = False
        self.has_rapids = False
        self.has_numba = False
        self.has_xgboost_gpu = False
        self.gpu_count = 0
        self.gpu_memory = {}
        self.backend = 'cpu'  # cpu, cuda, rapids
        
        self._detect_hardware()
        self._configure_backend()
    
    def _detect_hardware(self):
        """Detect available hardware and libraries."""
        # Check for CUDA
        try:
            import torch
            self.has_cuda = torch.cuda.is_available()
            if self.has_cuda:
                self.gpu_count = torch.cuda.device_count()
                for i in range(self.gpu_count):
                    props = torch.cuda.get_device_properties(i)
                    self.gpu_memory[i] = props.total_memory / (1024**3)  # GB
        except ImportError:
            try:
                # Try CuPy for CUDA detection
                import cupy as cp
                self.has_cuda = True
                self.gpu_count = cp.cuda.runtime.getDeviceCount()
            except (ImportError, Exception):
                pass
        
        # Check for RAPIDS
        try:
            import cudf
            import cuml
            self.has_rapids = True
        except ImportError:
            pass
        
        # Check for Numba (JIT compilation)
        try:
            import numba
            self.has_numba = True
        except ImportError:
            pass
        
        # Check for XGBoost GPU support
        try:
            import xgboost as xgb
            self.has_xgboost_gpu = self.has_cuda
        except ImportError:
            pass
    
    def _configure_backend(self):
        """Configure the best available backend."""
        if self.has_rapids and self.has_cuda:
            self.backend = 'rapids'
        elif self.has_cuda:
            self.backend = 'cuda'
        else:
            self.backend = 'cpu'
    
    def get_dataframe_backend(self):
        """
        Get the best DataFrame backend.
        
        Returns:
            Module for DataFrame operations (cudf or pandas)
        """
        if self.backend == 'rapids':
            try:
                import cudf as df_backend
                return df_backend
            except ImportError:
                pass
        
        # Fallback to pandas
        import pandas as df_backend
        return df_backend
    
    def get_array_backend(self):
        """
        Get the best array backend.
        
        Returns:
            Module for array operations (cupy or numpy)
        """
        if self.backend in ['rapids', 'cuda']:
            try:
                import cupy as array_backend
                return array_backend
            except ImportError:
                pass
        
        # Fallback to numpy
        import numpy as array_backend
        return array_backend
    
    def get_ml_params(self) -> Dict[str, Any]:
        """
        Get ML parameters optimized for available hardware.
        
        Returns:
            Dictionary of ML parameters
        """
        params = {
            'tree_method': 'auto',
            'predictor': 'auto',
            'n_jobs': -1
        }
        
        if self.has_xgboost_gpu and self.has_cuda:
            params['tree_method'] = 'gpu_hist'
            params['predictor'] = 'gpu_predictor'
            params['gpu_id'] = 0
        elif self.has_numba:
            params['tree_method'] = 'hist'
        
        return params
    
    def get_dask_config(self) -> Dict[str, Any]:
        """
        Get Dask configuration for parallel processing.
        
        Returns:
            Dictionary of Dask configuration
        """
        config = {
            'scheduler': 'threads',
            'num_workers': os.cpu_count()
        }
        
        if self.has_cuda:
            config['scheduler'] = 'distributed'
        
        return config
    
    def optimize_for_batch_size(self, data_size: int) -> int:
        """
        Calculate optimal batch size for processing.
        
        Args:
            data_size: Total size of data to process
            
        Returns:
            Optimal batch size
        """
        if self.backend == 'rapids' and self.gpu_count > 0:
            # Use GPU memory to determine batch size
            avg_gpu_mem = sum(self.gpu_memory.values()) / len(self.gpu_memory)
            # Use 80% of GPU memory, estimate 1MB per item
            batch_size = int(avg_gpu_mem * 1024 * 0.8)
        elif self.backend == 'cuda':
            batch_size = 1000  # Conservative for CUDA
        else:
            # CPU: use reasonable batch size
            batch_size = min(100, data_size // 10)
        
        return max(1, min(batch_size, data_size))
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get HPC configuration information.
        
        Returns:
            Configuration info dictionary
        """
        return {
            'backend': self.backend,
            'has_cuda': self.has_cuda,
            'has_rapids': self.has_rapids,
            'has_numba': self.has_numba,
            'has_xgboost_gpu': self.has_xgboost_gpu,
            'gpu_count': self.gpu_count,
            'gpu_memory_gb': self.gpu_memory,
            'cpu_count': os.cpu_count()
        }
    
    def print_info(self):
        """Print HPC configuration information."""
        info = self.get_info()
        
        print("=" * 60)
        print("⚡ HPC Configuration")
        print("=" * 60)
        print(f"Backend: {info['backend'].upper()}")
        print(f"CPU Cores: {info['cpu_count']}")
        print(f"CUDA Available: {'✅' if info['has_cuda'] else '❌'}")
        print(f"RAPIDS Available: {'✅' if info['has_rapids'] else '❌'}")
        print(f"Numba JIT Available: {'✅' if info['has_numba'] else '❌'}")
        print(f"XGBoost GPU: {'✅' if info['has_xgboost_gpu'] else '❌'}")
        
        if info['gpu_count'] > 0:
            print(f"\n🎮 GPU Information:")
            print(f"GPU Count: {info['gpu_count']}")
            for gpu_id, memory in info['gpu_memory_gb'].items():
                print(f"  GPU {gpu_id}: {memory:.2f} GB")
        
        print("=" * 60)
    
    def enable_optimizations(self):
        """Enable various optimizations based on available hardware."""
        # Set environment variables for optimal performance
        if self.has_cuda:
            os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(map(str, range(self.gpu_count)))
        
        if self.has_numba:
            os.environ['NUMBA_CACHE_DIR'] = '/tmp/numba_cache'
            os.environ['NUMBA_NUM_THREADS'] = str(os.cpu_count())
        
        # Suppress warnings for cleaner output
        warnings.filterwarnings('ignore', category=FutureWarning)


# Global HPC configuration instance
_hpc_config = None


def get_hpc_config() -> HPCConfig:
    """
    Get the global HPC configuration instance.
    
    Returns:
        HPCConfig instance
    """
    global _hpc_config
    if _hpc_config is None:
        _hpc_config = HPCConfig()
        _hpc_config.enable_optimizations()
    return _hpc_config
