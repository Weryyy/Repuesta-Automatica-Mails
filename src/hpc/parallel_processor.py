"""
Parallel Processor - Handles parallel and distributed processing of data.
"""
import os
from typing import List, Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp


class ParallelProcessor:
    """Handles parallel processing of data using various backends."""
    
    def __init__(self, hpc_config=None):
        """
        Initialize parallel processor.
        
        Args:
            hpc_config: HPCConfig instance
        """
        if hpc_config is None:
            from .config import get_hpc_config
            hpc_config = get_hpc_config()
        
        self.hpc_config = hpc_config
        self.num_workers = os.cpu_count() or 4
    
    def map_parallel(self, func: Callable, data: List[Any], 
                     use_processes: bool = False,
                     batch_size: Optional[int] = None) -> List[Any]:
        """
        Apply function to data in parallel.
        
        Args:
            func: Function to apply
            data: List of data items
            use_processes: Use processes instead of threads
            batch_size: Optional batch size for processing
            
        Returns:
            List of results
        """
        if not data:
            return []
        
        # Determine batch size
        if batch_size is None:
            batch_size = self.hpc_config.optimize_for_batch_size(len(data))
        
        # Choose executor
        if use_processes:
            executor_class = ProcessPoolExecutor
        else:
            executor_class = ThreadPoolExecutor
        
        # Process in parallel
        results = []
        with executor_class(max_workers=self.num_workers) as executor:
            # Process in batches
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                batch_results = list(executor.map(func, batch))
                results.extend(batch_results)
        
        return results
    
    def process_dataframe_parallel(self, df, func: Callable, 
                                   chunk_size: Optional[int] = None) -> Any:
        """
        Process DataFrame in parallel chunks.
        
        Args:
            df: DataFrame (pandas or cudf)
            func: Function to apply to each chunk
            chunk_size: Size of chunks
            
        Returns:
            Processed result
        """
        # Get DataFrame backend
        df_backend = self.hpc_config.get_dataframe_backend()
        
        # Determine chunk size
        if chunk_size is None:
            chunk_size = max(100, len(df) // self.num_workers)
        
        # Split into chunks
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        
        # Process chunks in parallel
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(executor.map(func, chunks))
        
        # Combine results
        if hasattr(df_backend, 'concat'):
            return df_backend.concat(results)
        else:
            # Fallback for other types
            return results
    
    def process_with_dask(self, data, func: Callable) -> Any:
        """
        Process data using Dask for distributed computing.
        
        Args:
            data: Data to process
            func: Function to apply
            
        Returns:
            Processed result
        """
        try:
            import dask
            import dask.bag as db
            
            # Create Dask bag
            bag = db.from_sequence(data, npartitions=self.num_workers)
            
            # Apply function
            result = bag.map(func).compute()
            
            return result
        except ImportError:
            # Fallback to regular parallel processing
            return self.map_parallel(func, data)
    
    def process_xarray(self, xarr, func: Callable, dim: str = 'time') -> Any:
        """
        Process xarray data in parallel.
        
        Args:
            xarr: xarray Dataset or DataArray
            func: Function to apply
            dim: Dimension to process along
            
        Returns:
            Processed xarray
        """
        try:
            import xarray as xr
            import dask
            
            # Use Dask for parallel processing
            if not xarr.chunks:
                xarr = xarr.chunk({dim: 'auto'})
            
            # Apply function
            result = xarr.map_blocks(func)
            
            return result
        except ImportError:
            raise RuntimeError("xarray not installed. Install with: pip install xarray")
    
    def batch_process(self, data: List[Any], func: Callable,
                     batch_size: Optional[int] = None,
                     progress_callback: Optional[Callable] = None) -> List[Any]:
        """
        Process data in batches with optional progress callback.
        
        Args:
            data: Data to process
            func: Function to apply
            batch_size: Size of batches
            progress_callback: Callback(current, total) for progress
            
        Returns:
            List of results
        """
        if batch_size is None:
            batch_size = self.hpc_config.optimize_for_batch_size(len(data))
        
        results = []
        total_batches = (len(data) + batch_size - 1) // batch_size
        
        for i, batch_idx in enumerate(range(0, len(data), batch_size)):
            batch = data[batch_idx:batch_idx + batch_size]
            batch_results = [func(item) for item in batch]
            results.extend(batch_results)
            
            if progress_callback:
                progress_callback(i + 1, total_batches)
        
        return results
    
    def async_process(self, data: List[Any], func: Callable) -> List[Any]:
        """
        Process data asynchronously.
        
        Args:
            data: Data to process
            func: Async function to apply
            
        Returns:
            List of results
        """
        import asyncio
        
        async def process_all():
            tasks = [func(item) for item in data]
            return await asyncio.gather(*tasks)
        
        # Run async processing
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(process_all())
        
        return results


class GPUProcessor:
    """Handles GPU-accelerated processing."""
    
    def __init__(self, hpc_config=None):
        """
        Initialize GPU processor.
        
        Args:
            hpc_config: HPCConfig instance
        """
        if hpc_config is None:
            from .config import get_hpc_config
            hpc_config = get_hpc_config()
        
        self.hpc_config = hpc_config
        
        if not hpc_config.has_cuda:
            raise RuntimeError("CUDA not available for GPU processing")
    
    def to_gpu(self, data):
        """
        Transfer data to GPU.
        
        Args:
            data: Data to transfer (numpy array, pandas DataFrame, etc.)
            
        Returns:
            GPU data (cupy array, cudf DataFrame, etc.)
        """
        if self.hpc_config.has_rapids:
            import cudf
            if hasattr(data, 'to_gpu'):
                return data.to_gpu()
            elif isinstance(data, list):
                return cudf.DataFrame(data)
        
        # Fallback to cupy
        try:
            import cupy as cp
            return cp.asarray(data)
        except ImportError:
            raise RuntimeError("No GPU backend available")
    
    def to_cpu(self, data):
        """
        Transfer data from GPU to CPU.
        
        Args:
            data: GPU data
            
        Returns:
            CPU data
        """
        if hasattr(data, 'to_pandas'):
            return data.to_pandas()
        elif hasattr(data, 'get'):
            return data.get()
        else:
            return data
    
    def process_on_gpu(self, data, func: Callable):
        """
        Process data on GPU.
        
        Args:
            data: Data to process
            func: Function to apply (must support GPU operations)
            
        Returns:
            Processed data
        """
        # Transfer to GPU
        gpu_data = self.to_gpu(data)
        
        # Process
        result = func(gpu_data)
        
        # Transfer back to CPU
        return self.to_cpu(result)
