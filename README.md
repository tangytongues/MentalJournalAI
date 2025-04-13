# Mind Journal - Mental Health Journal & Mood Tracker

A sophisticated journal application with NLP-powered mood analysis and mental health tracking. This web application helps users track their mental health journey by analyzing their journal entries and providing useful insights and resources.

## Features

- **User Authentication**: Secure account creation and login system
- **Journal Entries**: Write and save personal journal entries
- **Sentiment Analysis**: Automatic analysis of mood and emotions in journal entries
- **Mood Tracking**: Visualize your mood patterns over time through charts
- **Emotion Detection**: Identify primary emotions expressed in your writing
- **Mental Health Signal Detection**: Recognize potential anxiety, stress, or depression signals
- **Personalized Resources**: Get mental health resources based on your journal content
- **Insightful Dashboard**: See a summary of your journal and mood trends

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Setup Instructions

1. **Clone or download this repository**

2. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages**:
   ```
   pip install -r requirements_list.txt
   ```

5. **Download the required NLTK data**:
   ```python
   python -m nltk.downloader vader_lexicon
   python -m nltk.downloader punkt
   ```

6. **Download the required spaCy model**:
   ```
   python -m spacy download en_core_web_sm
   ```

7. **Run the application**:
   ```
   python app.py
   ```

8. **Access the application** in your web browser at `http://localhost:5000`

## Database

The application uses SQLite by default, with the database file stored in the `instance` folder. No additional database configuration is required for local use.

## Usage

1. **Register an account** or log in if you already have one
2. **Create journal entries** from the journal page
3. **View insights** on your mood and emotional patterns
4. **Explore resources** related to your mental health

## Project Structure

- `app.py`: Main application file with routes and configuration
- `models.py`: Database models for users, journal entries, and mood data
- `utils/`: Utility modules
  - `nlp_utils.py`: NLP functions for sentiment analysis and emotion detection
  - `chart_utils.py`: Functions for generating chart data
- `static/`: Static files (CSS, JavaScript)
  - `css/custom.css`: Custom styles
  - `js/`: JavaScript files for charts and UI functionality
- `templates/`: HTML templates for the application
- `instance/`: Contains the SQLite database file

## Note

This application is designed for personal use and educational purposes. It is not intended to replace professional mental health services. The mental health analysis is based on simple natural language processing techniques and should not be considered as clinical advice.

## License

This project is open-source and available for personal and educational use.
Created by @tangy_tongues
