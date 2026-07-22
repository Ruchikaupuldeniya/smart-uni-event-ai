import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="UniEvent AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Styling Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #6C63FF;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5750D1;
        transform: scale(1.02);
    }
    /* Hide default Streamlit footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2941/2941572.png", width=120)
    st.title("UniEvent AI")
    st.markdown("Your Smart Campus Assistant")
    st.markdown("---")
    menu = st.radio("📌 Select Feature", ["🏠 Home", "🎯 Event Recommendations", "📈 Turnout Predictor", "🏛️ Smart Scheduler", "📊 Analytics & Sentiment"])
    st.markdown("---")
    st.caption("⚙️ Powered by Machine Learning & NLP")

# ==========================================
# HOME PAGE
# ==========================================
if menu == "🏠 Home":
    st.title("Welcome to UniEvent AI 🎓")
    st.markdown("### The Next-Generation University Event Portal")
    st.write("This platform uses Artificial Intelligence to enhance the campus experience for both students and organizers. Select a tool from the sidebar to get started!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **For Students:** Find events that perfectly match your interests using our AI Recommendation Engine.")
        st.warning("⚠️ **For Organizers:** Avoid empty halls! Predict how many students will attend your event before booking the venue.")
    with col2:
        st.success("🏛️ **For Admins:** Resolve venue conflicts effortlessly and read real-time student sentiment analysis.")

# ==========================================
# EVENT RECOMMENDATIONS
# ==========================================
elif menu == "🎯 Event Recommendations":
    st.title("🎯 Find Your Next Favorite Event")
    st.markdown("Enter your Student ID, and our AI will fetch the best events based on your unique profile.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        student_id = st.text_input("Enter Student ID:", placeholder="e.g., S0001, S0150")
        submit = st.button("✨ Get Recommendations")
    
    if submit:
        if student_id:
            # Interactive Progress Bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
                if i == 30: status_text.text("Scanning student profile...")
                if i == 60: status_text.text("Calculating Cosine Similarity matrix...")
                if i == 90: status_text.text("Fetching best matches...")
                
            status_text.empty()
            progress_bar.empty()
            
            try:
                res = requests.get(f"{API_URL}/recommend/{student_id.strip()}")
                if res.status_code == 200:
                    recs = res.json()["recommendations"]
                    st.success("✅ Analysis Complete! Here are your top matches:")
                    
                    # Display as interactive cards using columns
                    for i, rec in enumerate(recs):
                        with st.expander(f"🏅 Match #{i+1}: {rec['name']} (Score: {rec['score'] * 100:.1f}%)", expanded=(i==0)):
                            st.write(f"**Category:** {rec['category']}")
                            st.write("Don't miss out on this amazing opportunity tailored just for you!")
                            st.button(f"RSVP Now", key=f"rsvp_{i}")
                            
                else:
                    st.error("Student not found. Please try another ID.")
            except Exception as e:
                st.error("⚠️ Connection Error. Ensure Backend API is running.")
        else:
            st.toast("Please enter a Student ID first!", icon="⚠️")

# ==========================================
# TURNOUT PREDICTOR
# ==========================================
elif menu == "📈 Turnout Predictor":
    st.title("📈 AI Turnout Predictor")
    st.markdown("Don't guess! Let our **Random Forest Regressor** predict the exact crowd size.")
    
    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Select Category", ["Hackathon", "Musical Show", "Sports Meet", "Tech Talk", "Career Fair", "Workshop", "Cultural Event"])
            venue_cap = st.slider("Expected Venue Capacity", min_value=50, max_value=2000, step=50, value=500)
        with col2:
            event_date = st.date_input("Event Date", datetime.now())
            
        submitted = st.form_submit_button("🔮 Predict Crowd Size")
        
    if submitted:
        with st.spinner("Crunching numbers through the Random Forest..."):
            time.sleep(1) # Fake delay for better UX
            payload = {"category": category, "venue_capacity": venue_cap, "date": event_date.strftime("%Y-%m-%d")}
            try:
                res = requests.post(f"{API_URL}/predict_turnout", json=payload)
                if res.status_code == 200:
                    turnout = res.json()["predicted_turnout"]
                    
                    st.toast("Prediction Generated Successfully!", icon="✅")
                    
                    # Beautiful Metric Display
                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res2.metric(label="Expected Students", value=turnout, delta=f"{turnout - venue_cap} vs Capacity", delta_color="inverse")
                    
                    if turnout > venue_cap:
                        st.error(f"🚨 DANGER: You are over capacity by {turnout - venue_cap} people! Please book a larger hall.")
                    elif turnout < (venue_cap * 0.3):
                        st.warning("⚠️ Warning: Hall might look empty. Consider a smaller, cozier venue.")
                    else:
                        st.balloons()
                        st.success("🎉 Perfect match! Your venue is perfectly sized for the expected crowd.")
            except:
                st.error("⚠️ Connection Error.")

# ==========================================
# SMART SCHEDULER
# ==========================================
elif menu == "🏛️ Smart Scheduler":
    st.title("🏛️ Conflict Resolution Engine")
    st.markdown("Two events fighting for the Main Hall? Let AI decide based on expected attendance.")
    
    st.write("---")
    colA, colB = st.columns(2)
    with colA:
        st.subheader("🔴 Event A")
        e1_name = st.text_input("Name", "Tech Summit 2026", key="e1n")
        e1_cat = st.selectbox("Category", ["Hackathon", "Tech Talk", "Workshop"], key="e1c")
        e1_date = st.date_input("Date", datetime.now(), key="e1d")
        
    with colB:
        st.subheader("🔵 Event B")
        e2_name = st.text_input("Name", "Acoustic Night", key="e2n")
        e2_cat = st.selectbox("Category", ["Musical Show", "Cultural Event", "Sports Meet"], key="e2c")
        e2_date = st.date_input("Date", datetime.now(), key="e2d")
        
    if st.button("⚖️ Resolve Conflict via AI"):
        with st.spinner("Analyzing historical data to resolve conflict..."):
            time.sleep(1.5)
            payload = {
                "event1_name": e1_name, "event1_category": e1_cat, "event1_venue_capacity": 500, "event1_date": e1_date.strftime("%Y-%m-%d"),
                "event2_name": e2_name, "event2_category": e2_cat, "event2_venue_capacity": 500, "event2_date": e2_date.strftime("%Y-%m-%d")
            }
            try:
                res = requests.post(f"{API_URL}/resolve_conflict", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.write("### AI Analysis Results:")
                    st.progress(data['event1_turnout'] / (data['event1_turnout'] + data['event2_turnout']), text=f"{e1_name} vs {e2_name} Crowd Share")
                    
                    c1, c2 = st.columns(2)
                    c1.metric(e1_name, f"{data['event1_turnout']} pax")
                    c2.metric(e2_name, f"{data['event2_turnout']} pax")
                    
                    st.success(f"**Final Verdict:** {data['recommendation']}")
            except:
                st.error("Error making prediction.")

# ==========================================
# ANALYTICS & SENTIMENT
# ==========================================
elif menu == "📊 Analytics & Sentiment":
    st.title("📊 Admin Dashboard & Sentiment AI")
    
    st.subheader("💬 Live Sentiment Analyzer")
    st.write("Type a sample student review below, and our NLP engine will classify its sentiment.")
    
    review = st.text_input("Enter review:", "The hackathon was brilliant but the food was a bit cold.")
    if st.button("Analyze Sentiment"):
        try:
            res = requests.post(f"{API_URL}/analyze_sentiment", json={"feedback": review})
            if res.status_code == 200:
                sent = res.json()["sentiment"]
                pol = res.json()["polarity"]
                
                if sent == "Positive":
                    st.success(f"😊 **{sent}** (Score: {pol:.2f})")
                elif sent == "Negative":
                    st.error(f"😠 **{sent}** (Score: {pol:.2f})")
                else:
                    st.info(f"😐 **{sent}** (Score: {pol:.2f})")
        except:
            st.error("API Connection Error")
            
    st.write("---")
    st.subheader("📈 University Insights")
    
    try:
        students_df = pd.read_csv(os.path.join(DATA_DIR, 'students.csv'))
        events_df = pd.read_csv(os.path.join(DATA_DIR, 'events.csv'))
        attendance_df = pd.read_csv(os.path.join(DATA_DIR, 'attendance.csv'))
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Registered Students", f"{len(students_df):,}")
        c2.metric("Total Events Hosted", len(events_df))
        c3.metric("Total Attendance Records", f"{len(attendance_df):,}")
        
        st.write("---")
        
        # Dashboard Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 📅 Events by Category")
            category_counts = events_df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            st.bar_chart(category_counts.set_index('Category'), color="#6C63FF")
            
        with col_chart2:
            st.markdown("#### 🎓 Student Distribution by University")
            uni_counts = students_df['university'].value_counts().reset_index()
            uni_counts.columns = ['University', 'Count']
            st.bar_chart(uni_counts.set_index('University'), color="#FF6C63")
        
        st.write("### 🔎 Data Explorer")
        st.write("You can interact with the raw data below (sort, filter, search).")
        st.dataframe(events_df, use_container_width=True)
    except:
        st.warning("Data files not found.")
