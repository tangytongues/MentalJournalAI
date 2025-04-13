"""
Utilities for generating chart data
"""

from datetime import datetime, timedelta
import json
from models import MoodData

def generate_mood_data(user_id, days=30):
    """
    Generate mood data for the specified number of days.
    Returns a dictionary with dates, sentiment scores, and emotions.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Query the mood data for the specified time range
    mood_entries = MoodData.query.filter(
        MoodData.user_id == user_id,
        MoodData.date >= start_date,
        MoodData.date <= end_date
    ).order_by(MoodData.date.asc()).all()
    
    # Create a dictionary to store the data
    data = {
        "dates": [],
        "sentiment_scores": [],
        "emotions": []
    }
    
    # If no mood data exists, return empty data
    if not mood_entries:
        return data
    
    # Convert to arrays for Chart.js
    for entry in mood_entries:
        # Format date as MM/DD
        date_str = entry.date.strftime('%m/%d')
        data["dates"].append(date_str)
        
        # Scale sentiment from [-1, 1] to [0, 10] for better visualization
        scaled_sentiment = (entry.sentiment_score + 1) * 5
        data["sentiment_scores"].append(round(scaled_sentiment, 1))
        
        # Add primary emotion
        data["emotions"].append(entry.primary_emotion)
    
    return data

def generate_emotion_distribution(user_id, days=30):
    """
    Generate emotion distribution data for the specified number of days.
    Returns a dictionary with emotion categories and their frequencies.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Query the mood data for the specified time range
    mood_entries = MoodData.query.filter(
        MoodData.user_id == user_id,
        MoodData.date >= start_date,
        MoodData.date <= end_date
    ).all()
    
    # Count occurrences of each emotion
    emotion_counts = {}
    
    for entry in mood_entries:
        if entry.primary_emotion:
            if entry.primary_emotion in emotion_counts:
                emotion_counts[entry.primary_emotion] += 1
            else:
                emotion_counts[entry.primary_emotion] = 1
    
    # Convert to arrays for Chart.js
    labels = list(emotion_counts.keys())
    values = list(emotion_counts.values())
    
    return {
        "labels": labels,
        "values": values
    }
