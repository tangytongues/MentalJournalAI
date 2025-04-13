# Local Installation Instructions

This document provides detailed instructions to set up Mind Journal on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Step-by-Step Installation

### 1. Download or Clone the Repository

- Option 1: Download the ZIP file and extract it to a folder on your computer
- Option 2: Clone using Git: `git clone <repository-url>`

### 2. Create a Virtual Environment

Navigate to the project directory in your terminal:

```bash
cd mind-journal
```

Create a virtual environment:

- Windows:
  ```bash
  python -m venv venv
  ```

- macOS/Linux:
  ```bash
  python3 -m venv venv
  ```

### 3. Activate the Virtual Environment

- Windows:
  ```bash
  venv\Scripts\activate
  ```

- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Required Packages

Install all the required dependencies:

```bash
pip install -r requirements-local.txt
```

### 5. Download NLP Resources

Run the following commands to download the necessary NLP models:

```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
python -m spacy download en_core_web_sm
```

### 6. Run the Application

Start the Flask application:

```bash
python app.py
```

The application should now be running at `http://localhost:5000` or `http://127.0.0.1:5000`.

### 7. Create an Account

- Open your browser and navigate to the application URL
- Click on "Register" to create a new account
- Start using your journal!

## Troubleshooting

If you encounter any issues during installation:

1. Make sure all Python dependencies are installed correctly
2. Check that the required NLTK and spaCy models were downloaded successfully
3. Verify that the SQLite database file has been created (it should be named `journal.db` in the application directory)
4. Check the terminal for any error messages

## Database Management

By default, the application uses SQLite for local development. The database file will be created automatically when you run the application for the first time.

If you need to reset the database, you can delete the `journal.db` file and restart the application.

## Notes for Production Deployment

For production use:

1. Set a secure `SESSION_SECRET` environment variable
2. Consider using a more robust database like PostgreSQL
3. Implement proper backup procedures for your data
4. Set `debug=False` in the app.run() call in app.py