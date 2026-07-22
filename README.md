# 🎓 Smart University Event Portal (AI-Powered)

An Enterprise-grade AI Solution for University Event Management. 
This project leverages Machine Learning and Natural Language Processing (NLP) to revolutionize how university events are organized, scheduled, and attended.

## 🚀 Features
- **Event Recommendation Engine (Content-Based Filtering):** Recommends tailored events to students based on their interests and past attendance using TF-IDF and Cosine Similarity.
- **AI Turnout Predictor (Random Forest Regression):** Predicts exactly how many students will attend an event based on historical data, category, and venue capacity.
- **Smart Venue Scheduler:** Resolves venue booking conflicts by comparing predicted turnout for competing events and allocating halls efficiently.
- **Live Sentiment Analysis (NLP):** Analyzes student feedback (Positive/Negative/Neutral) using TextBlob to provide organizers with actionable insights.
- **Admin Analytics Dashboard:** An interactive data explorer and KPI tracker for university administrators.

## 🛠️ Technology Stack
- **Machine Learning:** `scikit-learn`, `pandas`, `TextBlob` (NLP)
- **Backend API:** `FastAPI`, `Uvicorn`
- **Frontend UI:** `Streamlit`

## 💻 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI Backend**
   ```bash
   uvicorn api.main:app --reload
   ```

4. **Start the Streamlit Frontend** (Open a new terminal)
   ```bash
   streamlit run frontend/app.py
   ```

## 🧠 Model Training (Optional)
If you wish to generate new mock data and retrain the models:
```bash
python src/data_gen.py
python src/train.py
```
