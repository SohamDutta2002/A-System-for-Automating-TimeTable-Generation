# main.py
import argparse
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import data ingestion components
from src.data_ingestion_process.data_loader import DataLoader
from src.data_ingestion_process.data_validator import DataValidator
from src.data_ingestion_process.data_transformer import DataTransformer

# Import algorithm components
from src.hybrid_algorithm import HybridAlgorithm
from src.genetic_algorithms import GeneticAlgorithm
from src.simulated_annealing import SimulatedAnnealing
from src.constraint_programming import ConstraintProgramming

def main():
    """Main entry point for the timetable generation system."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Timetable Generation System")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("--algorithm", choices=["ga", "sa", "cp", "hybrid"], 
                      default="hybrid", help="Algorithm to use (default: hybrid)")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--visualize", action="store_true", help="Visualize results")
    args = parser.parse_args()
    
    # Initialize data ingestion pipeline
    loader = DataLoader()
    validator = DataValidator()
    transformer = DataTransformer()
    
    # Load and process input data
    try:
        logger.info(f"Processing input file: {args.input_file}")
        raw_data = loader.load_data(args.input_file)
        validation_result = validator.validate(raw_data)
        
        if not validation_result["is_valid"]:
            logger.error(f"Data validation failed: {validation_result['errors']}")
            return 1
            
        processed_data = transformer.transform(raw_data)
        logger.info(f"Successfully processed input data")
        
        # Select and run the algorithm
        if args.algorithm == "ga":
            logger.info("Running Genetic Algorithm")
            algorithm = GeneticAlgorithm(processed_data)
        elif args.algorithm == "sa":
            logger.info("Running Simulated Annealing")
            algorithm = SimulatedAnnealing(processed_data)
        elif args.algorithm == "cp":
            logger.info("Running Constraint Programming")
            algorithm = ConstraintProgramming(processed_data)
        else:  # hybrid
            logger.info("Running Hybrid Algorithm")
            algorithm = HybridAlgorithm(processed_data)
            
        # Execute the algorithm
        result = algorithm.run()
        
        # Save the result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = args.output or f"data/output/timetable_{timestamp}.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        loader.save_data(result, output_path)
        logger.info(f"Results saved to {output_path}")
        
        # Visualize if requested
        if args.visualize:
            from src.utils import visualize_timetable
            visualize_timetable(result, processed_data)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
