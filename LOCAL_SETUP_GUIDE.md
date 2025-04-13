# Mind Journal Local Setup Guide

This guide provides detailed instructions on how to download, set up, and run the Mind Journal application on your local machine.

## Step 1: Download the Project

1. Download the project files as a ZIP file.
2. Extract the ZIP file to a location of your choice on your computer.

## Step 2: Set Up a Python Environment

It's recommended to use a virtual environment to avoid package conflicts:

### Windows:
```
cd path\to\extracted\folder
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:
```
cd path/to/extracted/folder
python -m venv venv
source venv/bin/activate
```

## Step 3: Run the Setup Script

The setup script will install all required dependencies and download necessary NLP models:

```
python setup.py
```

This script performs the following actions:
- Checks your Python version
- Creates the instance directory for the database
- Installs required packages from requirements_list.txt
- Downloads NLTK data (vader_lexicon and punkt)
- Downloads the spaCy language model (en_core_web_sm)

## Step 4: Run the Application

After setup is complete, you can run the application with:

```
python run.py
```

The application will start, and you can access it in your web browser at: http://localhost:5000

## Step 5: Create an Account

When you first access the application, you'll need to:

1. Create a new user account by clicking on the "Register" link
2. Fill in your desired username, email, and password
3. Log in with your new credentials

## Troubleshooting

### Issue: Missing Dependencies
If you encounter errors about missing packages, try running:
```
pip install -r requirements_list.txt
```

### Issue: Missing NLTK Data
If the application fails because of missing NLTK data, run:
```
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

### Issue: Missing spaCy Model
If you see errors about missing spaCy models, run:
```
python -m spacy download en_core_web_sm
```

### Issue: Database Errors
If you encounter database errors, make sure the 'instance' directory exists and try:
```
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Database Information

- The application uses SQLite by default
- The database file is stored in the `instance` directory
- No additional database configuration is needed for local use

## Additional Notes

- The application will run in debug mode by default, so it will automatically reload when you make code changes
- All journal entries and user data are stored locally in the SQLite database
- The application does not send any data externally