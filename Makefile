# Mind Journal Makefile
# This Makefile contains helpful commands for managing the Mind Journal application

.PHONY: setup run clean reset help install-deps download-nltk download-spacy test backup

# Default target
help:
	@echo "Mind Journal Makefile Commands:"
	@echo "make setup        - Set up the application (install deps, download models)"
	@echo "make run          - Run the application"
	@echo "make install-deps - Install Python dependencies"
	@echo "make download-nltk - Download required NLTK data"
	@echo "make download-spacy - Download required spaCy model"
	@echo "make clean        - Remove Python cache files"
	@echo "make reset        - Reset the database"
	@echo "make backup       - Create a backup of the database"

# Setup the application
setup:
	@echo "Setting up Mind Journal application..."
	python setup.py

# Run the application
run:
	@echo "Starting Mind Journal application..."
	python run.py

# Install Python dependencies
install-deps:
	@echo "Installing dependencies..."
	pip install -r requirements_list.txt

# Download NLTK data
download-nltk:
	@echo "Downloading NLTK data..."
	python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

# Download spaCy model
download-spacy:
	@echo "Downloading spaCy model..."
	python -m spacy download en_core_web_sm

# Clean Python cache files
clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Reset the database
reset:
	@echo "Resetting the database..."
	@if [ -f instance/journal.db ]; then \
		echo "Creating backup of current database..."; \
		cp instance/journal.db instance/journal.db.backup; \
		echo "Removing current database..."; \
		rm instance/journal.db; \
		echo "Database reset. Running application will create a new database."; \
	else \
		echo "No database found to reset."; \
	fi

# Create a backup of the database
backup:
	@echo "Creating database backup..."
	@if [ -f instance/journal.db ]; then \
		cp instance/journal.db instance/journal.db.backup.$(shell date +%Y%m%d%H%M%S); \
		echo "Backup created at instance/journal.db.backup.$(shell date +%Y%m%d%H%M%S)"; \
	else \
		echo "No database found to backup."; \
	fi