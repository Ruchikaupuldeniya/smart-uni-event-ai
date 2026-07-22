from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from textblob import TextBlob

app = FastAPI(title="Smart University Event Recommender API")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load models and metadata on startup
try:
    tfidf = joblib.load(os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib'))
    event_vectors = joblib.load(os.path.join(MODELS_DIR, 'event_vectors.joblib'))
    events_df = pd.read_pickle(os.path.join(MODELS_DIR, 'events_metadata.pkl'))
    students_df = pd.read_pickle(os.path.join(MODELS_DIR, 'students_metadata.pkl'))
    turnout_model = joblib.load(os.path.join(MODELS_DIR, 'turnout_predictor.joblib'))
except Exception as e:
    print(f"Error loading models: {e}")

class PredictRequest(BaseModel):
    category: str
    venue_capacity: int
    date: str  # YYYY-MM-DD

class SentimentRequest(BaseModel):
    feedback: str

class ConflictRequest(BaseModel):
    event1_name: str
    event1_category: str
    event1_venue_capacity: int
    event1_date: str
    event2_name: str
    event2_category: str
    event2_venue_capacity: int
    event2_date: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the University Event API"}

@app.get("/recommend/{student_id}")
def recommend_events(student_id: str):
    student = students_df[students_df['student_id'] == student_id]
    if student.empty:
        raise HTTPException(status_code=404, detail="Student not found")
        
    interests = student.iloc[0]['interests']
    
    # Vectorize student interests
    student_vec = tfidf.transform([interests])
    
    # Calculate similarities
    similarities = cosine_similarity(student_vec, event_vectors).flatten()
    
    # Get top 5 recommendations
    top_indices = similarities.argsort()[-5:][::-1]
    
    recommendations = []
    for idx in top_indices:
        recommendations.append({
            "event_id": events_df.iloc[idx]['event_id'],
            "name": events_df.iloc[idx]['name'],
            "category": events_df.iloc[idx]['category'],
            "score": round(float(similarities[idx]), 3)
        })
        
    return {"student_id": student_id, "recommendations": recommendations}

@app.post("/predict_turnout")
def predict_turnout(req: PredictRequest):
    try:
        dt = datetime.strptime(req.date, "%Y-%m-%d")
        month = dt.month
        day_of_week = dt.weekday()
        
        # Create input dataframe
        input_data = pd.DataFrame([{
            'category': req.category,
            'venue_capacity': req.venue_capacity,
            'month': month,
            'day_of_week': day_of_week
        }])
        
        predicted = turnout_model.predict(input_data)[0]
        return {"predicted_turnout": int(predicted)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze_sentiment")
def analyze_sentiment(req: SentimentRequest):
    blob = TextBlob(req.feedback)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return {"sentiment": sentiment, "polarity": polarity}

@app.post("/resolve_conflict")
def resolve_conflict(req: ConflictRequest):
    try:
        dt1 = datetime.strptime(req.event1_date, "%Y-%m-%d")
        in1 = pd.DataFrame([{'category': req.event1_category, 'venue_capacity': req.event1_venue_capacity, 'month': dt1.month, 'day_of_week': dt1.weekday()}])
        turnout1 = int(turnout_model.predict(in1)[0])
        
        dt2 = datetime.strptime(req.event2_date, "%Y-%m-%d")
        in2 = pd.DataFrame([{'category': req.event2_category, 'venue_capacity': req.event2_venue_capacity, 'month': dt2.month, 'day_of_week': dt2.weekday()}])
        turnout2 = int(turnout_model.predict(in2)[0])
        
        if turnout1 > turnout2:
            recommendation = f"Allocate the larger hall to '{req.event1_name}' ({turnout1} students). Assign a smaller venue to '{req.event2_name}' ({turnout2} students)."
        elif turnout2 > turnout1:
            recommendation = f"Allocate the larger hall to '{req.event2_name}' ({turnout2} students). Assign a smaller venue to '{req.event1_name}' ({turnout1} students)."
        else:
            recommendation = f"Both events expect similar turnout ({turnout1} students). Venue capacity shouldn't be the deciding factor."
            
        return {
            "event1_turnout": turnout1,
            "event2_turnout": turnout2,
            "recommendation": recommendation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
