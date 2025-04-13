"""
NLP utilities for journal entry analysis
"""

import nltk
from textblob import TextBlob
import re
import logging
from collections import defaultdict
import spacy

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
    nltk.data.find('punkt')
except LookupError:
    nltk.download('vader_lexicon')
    nltk.download('punkt')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize NLP tools
sentiment_analyzer = SentimentIntensityAnalyzer()

# Try to load spaCy model, fall back to en_core_web_sm if available
try:
    nlp = spacy.load("en_core_web_sm")
    logging.info("Successfully loaded spaCy model: en_core_web_sm")
except OSError:
    try:
        # Try to download the model
        import subprocess
        import sys
        logging.info("spaCy model not found. Attempting to download en_core_web_sm...")
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info("Successfully downloaded spaCy model")
            nlp = spacy.load("en_core_web_sm")
        else:
            logging.warning(f"Failed to download spaCy model: {result.stderr}")
            logging.warning("Using TextBlob only for sentiment analysis")
            nlp = None
    except Exception as e:
        logging.warning(f"Error loading spaCy model: {str(e)}")
        logging.warning("Using TextBlob only for sentiment analysis")
        nlp = None

# Mental health signal keywords
MENTAL_HEALTH_SIGNALS = {
    "anxiety": [
        "anxious", "worried", "nervous", "panic", "fear", "dread", "restless",
        "tension", "stress", "overwhelm", "overthinking", "racing thoughts"
    ],
    "depression": [
        "depressed", "sad", "hopeless", "worthless", "empty", "numb", "tired",
        "exhausted", "lonely", "miserable", "unhappy", "meaningless", "unmotivated"
    ],
    "stress": [
        "stressed", "pressure", "overwhelmed", "burnt out", "burnout", "overworked",
        "deadline", "too much", "can't handle", "breaking point", "exhausted"
    ],
    "anger": [
        "angry", "furious", "mad", "rage", "irritated", "frustrated", "annoyed",
        "resentful", "hostile", "bitter", "enraged", "hate"
    ],
    "insomnia": [
        "can't sleep", "insomnia", "sleepless", "awake all night", "trouble sleeping",
        "sleep problems", "nightmares", "wake up early", "toss and turn"
    ]
}

def analyze_sentiment(text):
    """
    Analyze the sentiment of text using VADER.
    Returns a float from -1.0 (extremely negative) to 1.0 (extremely positive)
    """
    scores = sentiment_analyzer.polarity_scores(text)
    return scores['compound']

def analyze_emotion(text):
    """
    Analyze the emotional content of text.
    Returns a dictionary of emotion categories and their scores.
    """
    emotions = {
        "joy": ["happy", "delighted", "excited", "glad", "pleased", "joyful", "cheerful", "content"],
        "sadness": ["sad", "unhappy", "depressed", "gloomy", "miserable", "heartbroken", "blue", "down"],
        "anger": ["angry", "mad", "furious", "annoyed", "irritated", "enraged", "outraged", "hostile"],
        "fear": ["afraid", "scared", "frightened", "terrified", "anxious", "worried", "nervous", "fearful"],
        "surprise": ["surprised", "amazed", "astonished", "shocked", "startled", "stunned", "unexpected"],
        "disgust": ["disgusted", "repulsed", "revolted", "appalled", "sickened", "grossed", "nauseated"],
        "trust": ["trust", "confident", "secure", "reliant", "dependable", "reliable", "faith", "belief"],
        "anticipation": ["expect", "anticipate", "look forward", "hope", "await", "eager", "excited"]
    }
    
    # Normalize text: convert to lowercase and remove punctuation
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_text.split()
    
    # Count occurrences of emotion words
    emotion_counts = defaultdict(int)
    for emotion, keywords in emotions.items():
        for word in words:
            if word in keywords:
                emotion_counts[emotion] += 1
            # Check for phrases
            for keyword in keywords:
                if ' ' in keyword and keyword in text.lower():
                    emotion_counts[emotion] += 1
    
    # If spaCy is available, use it for better emotion analysis
    emotion_scores = defaultdict(float)
    if nlp:
        doc = nlp(text)
        # Process with spaCy for better context
        for emotion, keywords in emotions.items():
            for token in doc:
                if token.text.lower() in keywords:
                    # Consider intensifiers
                    for child in token.children:
                        if child.dep_ == "advmod" and child.text in ["very", "extremely", "really", "so"]:
                            emotion_counts[emotion] += 0.5
    
    # Normalize scores (if any emotions were detected)
    total_matches = sum(emotion_counts.values())
    if total_matches > 0:
        for emotion in emotion_counts:
            emotion_scores[emotion] = emotion_counts[emotion] / total_matches
    else:
        # If no emotions detected, use TextBlob polarity to estimate
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.2:
            emotion_scores["joy"] = 0.6
            emotion_scores["trust"] = 0.4
        elif polarity < -0.2:
            emotion_scores["sadness"] = 0.7
            emotion_scores["anger"] = 0.3
        else:
            # Neutral text
            emotion_scores["trust"] = 0.5
            emotion_scores["anticipation"] = 0.5
    
    # Ensure we return at least one emotion
    if not emotion_scores:
        emotion_scores["neutral"] = 1.0
        
    return dict(emotion_scores)

def detect_mental_health_signals(text):
    """
    Detect potential mental health signals in text.
    Returns a list of detected signal categories.
    """
    text_lower = text.lower()
    signals = []
    
    # Check for signal keywords
    for category, keywords in MENTAL_HEALTH_SIGNALS.items():
        for keyword in keywords:
            if keyword in text_lower:
                signals.append(category)
                break
    
    # Use TextBlob for additional sentiment analysis
    blob = TextBlob(text)
    
    # Check for severe negative sentiment
    if blob.sentiment.polarity < -0.5:
        if "depression" not in signals:
            signals.append("depression")
    
    # If using spaCy, do more sophisticated analysis
    if nlp:
        doc = nlp(text)
        
        # Check for first-person negative expressions
        for sent in doc.sents:
            # Look for patterns like "I feel worthless", "I can't handle", etc.
            for token in sent:
                if token.text.lower() in ["i", "me", "my", "myself"] and any(neg in sent.text.lower() for neg in ["can't", "cannot", "never", "no one", "worthless", "hopeless"]):
                    if "depression" not in signals:
                        signals.append("depression")
                    break
    
    return signals
