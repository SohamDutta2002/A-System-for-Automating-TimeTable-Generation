"""
Data Loader module for Timetable Generation System.
Handles loading JSON data files for the timetable generation algorithms.
"""

import json
import logging
import os
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoader:
    """
    Class for loading JSON data files containing timetable generation inputs.
    """
    
    def __init__(self):
        """Initialize the DataLoader."""
        pass
        
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing input data
            
        Returns:
            Dict[str, Any]: Loaded data as a dictionary
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        logger.info(f"Loading data from {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            error_msg = f"Input file not found: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Load and parse JSON data
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Successfully loaded data from {file_path}")
            return data
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON format in {file_path}: {str(e)}"
            logger.error(error_msg)
            raise
        
        except Exception as e:
            error_msg = f"Error loading data from {file_path}: {str(e)}"
            logger.error(error_msg)
            raise
    
    def save_data(self, data: Dict[str, Any], file_path: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data (Dict[str, Any]): Data to save
            file_path (str): Path where to save the JSON file
            
        Raises:
            IOError: If there's an issue writing to the file
        """
        logger.info(f"Saving data to {file_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Successfully saved data to {file_path}")
        
        except Exception as e:
            error_msg = f"Error saving data to {file_path}: {str(e)}"
            logger.error(error_msg)
            raise
