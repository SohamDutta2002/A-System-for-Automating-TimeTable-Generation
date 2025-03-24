"""
Data Ingestion Package for Timetable Generation System

This package handles the loading, validation, and transformation of input data
for the automated timetable generation system.

Created by: Arkaprabha Bera, Rupam Nandi, Soham Dutta, Akanksh Kumar Shaw
"""

__version__ = '1.0.0'
__author__ = 'Arkaprabha Bera, Rupam Nandi, Soham Dutta, Akanksh Kumar Shaw'

from .data_loader import DataLoader
from .data_validator import DataValidator
from .data_transformer import DataTransformer

# Create a convenience function for the entire data ingestion process
def process_input_data(file_path, config_path=None):
    """
    Complete data ingestion process: load, validate, and transform input data.
    
    Args:
        file_path (str): Path to the input JSON file
        config_path (str, optional): Path to configuration file for validation
        
    Returns:
        dict: Processed data ready for algorithm input
    """
    # Load data
    loader = DataLoader()
    raw_data = loader.load_data(file_path)
    
    # Validate data
    validator = DataValidator(config_path=config_path)
    validation_result = validator.validate(raw_data)
    if not validation_result['is_valid']:
        raise ValueError(f"Data validation failed: {validation_result['errors']}")
    
    # Transform data
    transformer = DataTransformer()
    processed_data = transformer.transform(raw_data)
    
    return processed_data
