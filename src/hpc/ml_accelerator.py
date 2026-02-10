"""
ML Accelerator - Accelerates machine learning operations with XGBoost and GPU support.
"""
from typing import Dict, Any, Optional, List
import numpy as np


class MLAccelerator:
    """Accelerates machine learning operations."""
    
    def __init__(self, hpc_config=None):
        """
        Initialize ML accelerator.
        
        Args:
            hpc_config: HPCConfig instance
        """
        if hpc_config is None:
            from .config import get_hpc_config
            hpc_config = get_hpc_config()
        
        self.hpc_config = hpc_config
        self.models = {}
    
    def create_classifier(self, model_id: str, params: Optional[Dict] = None) -> Any:
        """
        Create an optimized classifier.
        
        Args:
            model_id: Unique identifier for the model
            params: Model parameters
            
        Returns:
            Classifier model
        """
        try:
            import xgboost as xgb
            
            # Get optimal parameters
            default_params = self.hpc_config.get_ml_params()
            if params:
                default_params.update(params)
            
            # Create classifier
            model = xgb.XGBClassifier(**default_params)
            self.models[model_id] = model
            
            return model
        except ImportError:
            raise RuntimeError("XGBoost not installed. Install with: pip install xgboost")
    
    def create_regressor(self, model_id: str, params: Optional[Dict] = None) -> Any:
        """
        Create an optimized regressor.
        
        Args:
            model_id: Unique identifier for the model
            params: Model parameters
            
        Returns:
            Regressor model
        """
        try:
            import xgboost as xgb
            
            # Get optimal parameters
            default_params = self.hpc_config.get_ml_params()
            if params:
                default_params.update(params)
            
            # Create regressor
            model = xgb.XGBRegressor(**default_params)
            self.models[model_id] = model
            
            return model
        except ImportError:
            raise RuntimeError("XGBoost not installed")
    
    def train(self, model_id: str, X, y, eval_set: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Train a model.
        
        Args:
            model_id: Model identifier
            X: Training features
            y: Training labels
            eval_set: Optional evaluation set (X_eval, y_eval)
            
        Returns:
            Training results
        """
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        # Train
        if eval_set:
            model.fit(X, y, eval_set=[eval_set], verbose=False)
        else:
            model.fit(X, y)
        
        return {
            'model_id': model_id,
            'trained': True,
            'feature_count': X.shape[1] if hasattr(X, 'shape') else len(X[0])
        }
    
    def predict(self, model_id: str, X) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            model_id: Model identifier
            X: Features
            
        Returns:
            Predictions
        """
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        return model.predict(X)
    
    def predict_proba(self, model_id: str, X) -> np.ndarray:
        """
        Predict probabilities.
        
        Args:
            model_id: Model identifier
            X: Features
            
        Returns:
            Probability predictions
        """
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        return model.predict_proba(X)
    
    def get_feature_importance(self, model_id: str) -> Dict[int, float]:
        """
        Get feature importance.
        
        Args:
            model_id: Model identifier
            
        Returns:
            Feature importance dictionary
        """
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        importance = model.feature_importances_
        
        return {i: float(imp) for i, imp in enumerate(importance)}
    
    def save_model(self, model_id: str, filepath: str):
        """
        Save model to file.
        
        Args:
            model_id: Model identifier
            filepath: Path to save model
        """
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        model.save_model(filepath)
    
    def load_model(self, model_id: str, filepath: str):
        """
        Load model from file.
        
        Args:
            model_id: Model identifier
            filepath: Path to load model from
        """
        try:
            import xgboost as xgb
            
            # Create model
            if 'classifier' in model_id.lower():
                model = xgb.XGBClassifier()
            else:
                model = xgb.XGBRegressor()
            
            # Load
            model.load_model(filepath)
            self.models[model_id] = model
        except ImportError:
            raise RuntimeError("XGBoost not installed")
    
    def optimize_hyperparameters(self, model_id: str, X, y,
                                 param_grid: Dict[str, List],
                                 cv: int = 3) -> Dict[str, Any]:
        """
        Optimize model hyperparameters.
        
        Args:
            model_id: Model identifier
            X: Training features
            y: Training labels
            param_grid: Parameter grid for search
            cv: Cross-validation folds
            
        Returns:
            Best parameters and score
        """
        try:
            from sklearn.model_selection import GridSearchCV
            
            if model_id not in self.models:
                raise ValueError(f"Model {model_id} not found")
            
            model = self.models[model_id]
            
            # Grid search
            grid_search = GridSearchCV(
                model,
                param_grid,
                cv=cv,
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X, y)
            
            # Update model with best parameters
            self.models[model_id] = grid_search.best_estimator_
            
            return {
                'best_params': grid_search.best_params_,
                'best_score': grid_search.best_score_,
                'cv_results': grid_search.cv_results_
            }
        except ImportError:
            raise RuntimeError("scikit-learn not installed")


class NumbaAccelerator:
    """Accelerates numerical operations with Numba JIT compilation."""
    
    def __init__(self):
        """Initialize Numba accelerator."""
        try:
            import numba
            self.numba = numba
            self.available = True
        except ImportError:
            self.available = False
    
    def jit(self, func, **kwargs):
        """
        Apply JIT compilation to a function.
        
        Args:
            func: Function to compile
            **kwargs: Numba jit parameters
            
        Returns:
            Compiled function
        """
        if not self.available:
            return func
        
        return self.numba.jit(func, **kwargs)
    
    def vectorize(self, func, signatures=None):
        """
        Vectorize a function.
        
        Args:
            func: Function to vectorize
            signatures: Type signatures
            
        Returns:
            Vectorized function
        """
        if not self.available:
            return func
        
        if signatures:
            return self.numba.vectorize(signatures)(func)
        else:
            return self.numba.vectorize(func)
    
    def parallelize(self, func):
        """
        Parallelize a function.
        
        Args:
            func: Function to parallelize
            
        Returns:
            Parallelized function
        """
        if not self.available:
            return func
        
        return self.numba.jit(func, parallel=True)
