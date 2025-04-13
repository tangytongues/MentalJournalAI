# Mind Journal Download Checklist

To ensure you have all the necessary files for running the Mind Journal application locally, use this checklist to verify that all required files and directories are included in your download.

## Essential Files & Directories

### Core Application Files
- [ ] `app.py` - Main application file with Flask routes and configuration
- [ ] `models.py` - Database models for users, journal entries, mood data, and resources
- [ ] `main.py` - Entry point for the application
- [ ] `run.py` - Simple script to run the application locally
- [ ] `setup.py` - Setup script to install dependencies and prepare the environment
- [ ] `requirements_list.txt` - List of required Python packages

### Utility Scripts
- [ ] `utils/nlp_utils.py` - NLP utilities for sentiment analysis and emotion detection
- [ ] `utils/chart_utils.py` - Utilities for generating chart data

### Templates
- [ ] `templates/base.html` - Base template with layout and navigation
- [ ] `templates/login.html` - Login page
- [ ] `templates/register.html` - Registration page
- [ ] `templates/dashboard.html` - User dashboard
- [ ] `templates/journal.html` - Journal entry listing and creation
- [ ] `templates/entry.html` - Individual journal entry view
- [ ] `templates/insights.html` - Mood insights and analytics page
- [ ] `templates/resources.html` - Mental health resources page
- [ ] `templates/404.html` - Not found error page
- [ ] `templates/500.html` - Server error page

### Static Files
- [ ] `static/css/custom.css` - Custom CSS styling
- [ ] `static/js/journal.js` - JavaScript for journal functionality
- [ ] `static/js/mood_chart.js` - JavaScript for mood visualization
- [ ] `static/js/insights.js` - JavaScript for insights visualization

### Documentation
- [ ] `README.md` - Project overview and general instructions
- [ ] `LOCAL_SETUP_GUIDE.md` - Detailed guide for local setup

## Optional Items
- [ ] `instance/` directory - Will be created automatically to store your SQLite database
- [ ] `.gitignore` - Used for excluding files from version control if you're using Git

## Post-Download Steps

After verifying all files are present:

1. Follow the setup instructions in `LOCAL_SETUP_GUIDE.md`
2. Run the setup script: `python setup.py`
3. Start the application: `python run.py`
4. Access the application at: http://localhost:5000

## Troubleshooting Missing Files

If any essential files are missing, you can:

1. Download the project again
2. Check if the files were extracted properly from the ZIP file
3. Make sure you have the complete project structure with all subfolders