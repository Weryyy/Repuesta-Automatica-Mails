"""
Excel Writer Agent - Writes email data to Excel files.
"""
import os
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from .base_agent import BaseAgent


class ExcelWriterAgent(BaseAgent):
    """Agent for writing email data to Excel files."""
    
    def __init__(self, name: str = "ExcelWriter"):
        super().__init__(name)
        self.output_folder = "output"
        self.filename = None
    
    def configure(self, output_folder: str = "output", filename: str = None):
        """
        Configure the Excel writer.
        
        Args:
            output_folder: Folder to save Excel files
            filename: Custom filename (optional, auto-generated if not provided)
        """
        self.output_folder = output_folder
        self.filename = filename
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
    
    def execute(self, input_data: Any = None) -> str:
        """
        Write emails to an Excel file.
        
        Args:
            input_data: List of email dictionaries to write
        
        Returns:
            Path to the created Excel file
        """
        self.status = "executing"
        
        if not input_data or not isinstance(input_data, list):
            self.status = "error: No email data provided"
            self.output = None
            return self.output
        
        try:
            # Generate filename if not provided
            if not self.filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.filename = f"emails_{timestamp}.xlsx"
            
            # Full path
            filepath = os.path.join(self.output_folder, self.filename)
            
            # Convert emails to DataFrame
            df = pd.DataFrame(input_data)
            
            # Write to Excel
            df.to_excel(filepath, index=False, engine='openpyxl')
            
            self.output = filepath
            self.status = f"completed: {len(input_data)} emails written to {filepath}"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = None
        
        return self.output
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'output_folder': 'string (optional, default: output)',
            'filename': 'string (optional, auto-generated if not provided)'
        }
