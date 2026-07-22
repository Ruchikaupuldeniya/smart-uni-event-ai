import pandas as pd
import numpy as np
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

print("Loading data...")
students_df = pd.read_csv(os.path.join(DATA_DIR, 'students.csv'))
events_df = pd.read_csv(os.path.join(DATA_DIR, 'events.csv'))
attendance_df = pd.read_csv(os.path.join(DATA_DIR, 'attendance.csv'))

# ==========================================
# MODEL 1: Event Recommender (Content-Based)
# ==========================================
print("Training Event Recommender Model...")

# We will build a TF-IDF matrix for the event tags
# and recommend events based on a student's interests.

# Fill missing tags/interests with empty strings
events_df['tags'] = events_df['tags'].fillna('')
students_df['interests'] = students_df['interests'].fillna('')

# Fit a TF-IDF vectorizer on the event tags
tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit(events_df['tags'].tolist() + students_df['interests'].tolist())

# Transform event tags into vectors
event_vectors = tfidf.transform(events_df['tags'])

# Save the vectorizer and event vectors so the API can use them quickly
joblib.dump(tfidf, os.path.join(MODELS_DIR, 'tfidf_vectorizer.joblib'))
joblib.dump(event_vectors, os.path.join(MODELS_DIR, 'event_vectors.joblib'))
events_df.to_pickle(os.path.join(MODELS_DIR, 'events_metadata.pkl'))
students_df.to_pickle(os.path.join(MODELS_DIR, 'students_metadata.pkl'))

print("Recommender model saved!")

# ==========================================
# MODEL 2: Attendance (Turnout) Predictor
# ==========================================
print("Training Turnout Predictor Model...")

# Calculate actual turnout for each event
turnout_df = attendance_df[attendance_df['attended'] == 1].groupby('event_id').size().reset_index(name='turnout')

# Merge with events data
prediction_data = pd.merge(events_df, turnout_df, on='event_id', how='left')
prediction_data['turnout'] = prediction_data['turnout'].fillna(0)

# Feature Engineering
prediction_data['date'] = pd.to_datetime(prediction_data['date'])
prediction_data['month'] = prediction_data['date'].dt.month
prediction_data['day_of_week'] = prediction_data['date'].dt.dayofweek

# Select features and target
X = prediction_data[['category', 'venue_capacity', 'month', 'day_of_week']]
y = prediction_data['turnout']

# Preprocessing: One-hot encode the 'category'
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category'])
    ],
    remainder='passthrough' # Keep venue_capacity, month, day_of_week as is
)

# Create a pipeline with preprocessor and RandomForest Regressor
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
model_pipeline.fit(X, y)

# Save the trained model
joblib.dump(model_pipeline, os.path.join(MODELS_DIR, 'turnout_predictor.joblib'))

print("Turnout predictor model saved!")
print("Phase 3: Model Building Complete. All models saved in the 'models' directory.")
