# Timetable Generation Pipeline
PYTHON = python3
CONFIG_FILE = sample_data/input.json
OUTPUT_DIR = results
INTERIM_DIR = interim

.PHONY: all validate transform optimize assign_mentors clean test

all: validate transform optimize assign_mentors

validate:
	@echo "Validating input structure..."
	@mkdir -p $(INTERIM_DIR) $(OUTPUT_DIR)
	@$(PYTHON) data_ingestion/validator.py $(CONFIG_FILE)

transform: validate
	@echo "\nTransforming data for processing..."
	@$(PYTHON) data_ingestion/transformer.py $(CONFIG_FILE) $(INTERIM_DIR)/processed_data.pkl

optimize: transform
	@echo "\nRunning optimization algorithms..."
	@$(PYTHON) algo/genetic_algorithm.py \
		--input $(INTERIM_DIR)/processed_data.pkl \
		--output $(OUTPUT_DIR)/timetable.json \
		--config config/ga_params.json

assign_mentors: optimize
	@echo "\nAssigning mentor groups..."
	@$(PYTHON) algo/mentor_assigner.py \
		--timetable $(OUTPUT_DIR)/timetable.json \
		--output $(OUTPUT_DIR)/mentor_assignments.json

clean:
	@rm -rf $(INTERIM_DIR) $(OUTPUT_DIR)
	@echo "Cleaned all generated files"

test:
	@echo "Running test suite..."
	@pytest tests/ -v

install:
	@pip install -r requirements.txt

monitor:
	@watch -n 5 'tail -n 20 $(OUTPUT_DIR)/ga_log.txt'
