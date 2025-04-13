import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# JSON helper function for templates
def fromjson_filter(value):
    return json.loads(value)

# Initialize SQLAlchemy with a base class
class Base(DeclarativeBase):
    pass

# Create the Flask app
app = Flask(__name__)
# Use a secure secret key for local development - in production, use environment variables
app.secret_key = os.environ.get("SESSION_SECRET", "mind_journal_local_development_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Register the fromjson filter with Jinja
app.jinja_env.filters['fromjson'] = fromjson_filter

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///journal.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Import models and utils (after db initialization to avoid circular imports)
with app.app_context():
    from models import User, JournalEntry, MoodData, Resource
    from utils.nlp_utils import analyze_sentiment, analyze_emotion, detect_mental_health_signals
    from utils.chart_utils import generate_mood_data
    
    # Create database tables
    db.create_all()
    
    # Add default resources if none exist
    if not Resource.query.first():
        default_resources = [
            {
                "category": "anxiety",
                "title": "Deep Breathing Exercise",
                "content": "Practice the 4-7-8 breathing technique: Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds.",
                "link": "https://www.healthline.com/health/4-7-8-breathing"
            },
            {
                "category": "sadness",
                "title": "Gratitude Journaling",
                "content": "Write down three things you're grateful for today, no matter how small.",
                "link": "https://positivepsychology.com/gratitude-journal/"
            },
            {
                "category": "stress",
                "title": "Progressive Muscle Relaxation",
                "content": "Tense and then release each muscle group in your body, starting from your toes and moving up.",
                "link": "https://www.healthline.com/health/progressive-muscle-relaxation"
            },
            {
                "category": "general",
                "title": "Crisis Support Lines",
                "content": "If you're experiencing a mental health crisis, please reach out for support.",
                "link": "https://988lifeline.org/"
            }
        ]
        
        for resource_data in default_resources:
            resource = Resource(
                category=resource_data["category"],
                title=resource_data["title"],
                content=resource_data["content"],
                link=resource_data["link"]
            )
            db.session.add(resource)
        
        db.session.commit()

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "danger")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate form data
        if not username or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose another one.", "danger")
            return render_template("register.html")
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already registered. Please use another one.", "danger")
            return render_template("register.html")
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Main application routes
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login to access your dashboard.", "warning")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    user = User.query.get(user_id)
    
    # Get recent entries
    recent_entries = JournalEntry.query.filter_by(user_id=user_id).order_by(JournalEntry.date.desc()).limit(5).all()
    
    # Get mood data for the past 30 days
    mood_data = generate_mood_data(user_id, days=30)
    
    return render_template("dashboard.html", user=user, entries=recent_entries, mood_data=json.dumps(mood_data))

@app.route("/journal", methods=["GET", "POST"])
def journal():
    if "user_id" not in session:
        flash("Please login to access your journal.", "warning")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not title or not content:
            flash("Please provide both a title and content for your entry.", "danger")
            return redirect(url_for("journal"))
        
        # Analyze the journal entry content
        sentiment_score = analyze_sentiment(content)
        emotion_data = analyze_emotion(content)
        mental_health_signals = detect_mental_health_signals(content)
        
        # Create new journal entry
        new_entry = JournalEntry(
            title=title,
            content=content,
            date=datetime.now(),
            user_id=user_id,
            sentiment_score=sentiment_score,
            emotion_data=json.dumps(emotion_data),
            mental_health_signals=json.dumps(mental_health_signals)
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        # Create mood data entry
        mood_entry = MoodData(
            user_id=user_id,
            entry_id=new_entry.id,
            date=new_entry.date,
            sentiment_score=sentiment_score,
            primary_emotion=max(emotion_data.items(), key=lambda x: x[1])[0]
        )
        
        db.session.add(mood_entry)
        db.session.commit()
        
        flash("Journal entry saved successfully!", "success")
        return redirect(url_for("entry", entry_id=new_entry.id))
    
    # Get all entries for the user
    entries = JournalEntry.query.filter_by(user_id=user_id).order_by(JournalEntry.date.desc()).all()
    
    return render_template("journal.html", entries=entries)

@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    if "user_id" not in session:
        flash("Please login to view journal entries.", "warning")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    
    if not entry:
        flash("Entry not found or you don't have permission to view it.", "danger")
        return redirect(url_for("journal"))
    
    # Parse the JSON data
    emotion_data = json.loads(entry.emotion_data)
    mental_health_signals = json.loads(entry.mental_health_signals)
    
    # Get relevant resources based on detected signals
    resources = []
    if mental_health_signals:
        for signal in mental_health_signals:
            signal_resources = Resource.query.filter_by(category=signal.lower()).all()
            resources.extend(signal_resources)
    
    # Add general resources if we have fewer than 2 specific ones
    if len(resources) < 2:
        general_resources = Resource.query.filter_by(category="general").all()
        resources.extend(general_resources)
    
    # Remove duplicates while preserving order
    unique_resources = []
    resource_ids = set()
    for resource in resources:
        if resource.id not in resource_ids:
            unique_resources.append(resource)
            resource_ids.add(resource.id)
    
    return render_template("entry.html", entry=entry, emotion_data=emotion_data, 
                           mental_health_signals=mental_health_signals, resources=unique_resources[:3])

@app.route("/insights")
def insights():
    if "user_id" not in session:
        flash("Please login to view your insights.", "warning")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    
    # Get mood data for the past 60 days
    mood_data = generate_mood_data(user_id, days=60)
    
    # Get all entries for pattern analysis
    entries = JournalEntry.query.filter_by(user_id=user_id).order_by(JournalEntry.date.desc()).all()
    
    # Get emotion distributions
    emotions = {}
    signals = {}
    
    for entry in entries:
        emotion_data = json.loads(entry.emotion_data)
        for emotion, score in emotion_data.items():
            if emotion in emotions:
                emotions[emotion] += score
            else:
                emotions[emotion] = score
        
        mental_health_signals = json.loads(entry.mental_health_signals)
        for signal in mental_health_signals:
            if signal in signals:
                signals[signal] += 1
            else:
                signals[signal] = 1
    
    # Normalize emotion data
    total_emotion = sum(emotions.values())
    if total_emotion > 0:
        emotions = {k: (v / total_emotion) * 100 for k, v in emotions.items()}
    
    return render_template("insights.html", mood_data=json.dumps(mood_data), 
                           emotions=emotions, signals=signals, entries_count=len(entries))

@app.route("/resources")
def resources():
    if "user_id" not in session:
        flash("Please login to view resources.", "warning")
        return redirect(url_for("login"))
    
    # Get all resources, categorized
    categories = {}
    all_resources = Resource.query.all()
    
    for resource in all_resources:
        if resource.category not in categories:
            categories[resource.category] = []
        categories[resource.category].append(resource)
    
    return render_template("resources.html", categories=categories)

# API endpoints for AJAX requests
@app.route("/api/mood_data")
def api_mood_data():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    days = request.args.get("days", 30, type=int)
    
    mood_data = generate_mood_data(user_id, days=days)
    return jsonify(mood_data)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
