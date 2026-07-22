<div align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/2941/2941572.png" alt="Logo" width="120">
  
  # 🎓 Smart UniEvent AI Portal
  
  **An Enterprise-Grade, AI-Powered University Event Management Ecosystem**
  
  [![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://smart-uni-event-ai.streamlit.app/)
  [![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)]()
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()
  [![Machine Learning](https://img.shields.io/badge/Machine_Learning-Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)]()
</div>

<br />

## 💡 About The Project

Traditional university event management stops at scheduling and approvals. **Smart UniEvent AI** takes it a step further by leveraging Machine Learning and Natural Language Processing (NLP) to **Predict, Recommend, and Analyze** the entire university event ecosystem. 

Whether you are a student looking for the perfect hackathon or an admin trying to resolve double-booked venues, our AI has you covered.

## 🌟 Key Features

* **🎯 AI Event Recommender:** Uses *TF-IDF* and *Cosine Similarity* (Content-Based Filtering) to analyze a student's unique interests and recommend the perfect events.
* **📈 Turnout Predictor:** A *Random Forest Regression* model that accurately predicts how many students will attend an event, preventing over-booking or empty halls.
* **🏛️ Smart Venue Scheduler:** Automatically resolves venue booking conflicts by comparing expected turnout between competing events and recommending the optimal hall allocation.
* **💬 Live Sentiment Analysis:** Uses Natural Language Processing (*TextBlob*) to instantly classify student feedback (Positive/Negative/Neutral) to gauge event success.
* **📊 Interactive Admin Dashboard:** A sleek, real-time data explorer and KPI tracker built for university administrators.

## 🏗️ Architecture & Tech Stack

This project uses a modern decoupled architecture:

- **Frontend (UI):** [Streamlit](https://streamlit.io/) - Hosted on Streamlit Community Cloud.
- **Backend (API):** [FastAPI](https://fastapi.tiangolo.com/) - Serverless deployment on Vercel.
- **Machine Learning:** `scikit-learn`, `pandas`, `numpy`, `textblob`.

## 🚀 Live Demo

Experience the platform live: **[Smart UniEvent AI Dashboard](https://smart-uni-event-ai.streamlit.app/)**

> **Test Data:** Try entering Student IDs like `S0001`, `S0015`, or `S0150` in the Recommender tab!

## 💻 Getting Started (Local Development)

To run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/Ruchikaupuldeniya/smart-uni-event-ai.git
cd smart-uni-event-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Backend
Open a terminal and run the following command to start the AI engine:
```bash
uvicorn api.main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 4. Run the Streamlit Frontend
Open a **new terminal window** and run:
```bash
streamlit run frontend/app.py
```
*The dashboard will automatically open in your browser!*

## 🧠 Model Training & Data Generation

This project comes with synthetic data generated for a Sri Lankan university context. If you want to regenerate the data or retrain the models:

```bash
# 1. Generate new synthetic students, events, and reviews
python src/data_gen.py

# 2. Retrain the TF-IDF and Random Forest models
python src/train.py
```

## 📡 API Endpoints

Our FastAPI backend exposes the following key endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recommend/{student_id}` | `GET` | Returns top 5 personalized event recommendations for a student. |
| `/predict_turnout` | `POST` | Predicts the expected crowd for a planned event. |
| `/resolve_conflict` | `POST` | Compares two events and recommends which gets the larger venue. |
| `/analyze_sentiment` | `POST` | Returns polarity and sentiment label (Positive/Negative) for text. |

## 👨‍💻 Developed By

**Ruchika Upuldeniya** 
*Data Science Enthusiast | Machine Learning Developer*

If you like this project, don't forget to give it a ⭐ on GitHub!
