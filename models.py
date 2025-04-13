from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True)
    mood_data = db.relationship('MoodData', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sentiment_score = db.Column(db.Float)
    emotion_data = db.Column(db.Text)  # JSON string of emotion scores
    mental_health_signals = db.Column(db.Text)  # JSON array of detected signals
    mood_data = db.relationship('MoodData', backref='journal_entry', lazy=True, uselist=False)
    
    def __repr__(self):
        return f'<JournalEntry {self.title}>'
    
    def get_formatted_date(self):
        return self.date.strftime('%B %d, %Y at %I:%M %p')

class MoodData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('journal_entry.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    primary_emotion = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<MoodData {self.date} {self.sentiment_score}>'

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Resource {self.title}>'
