import streamlit as st
import datetime
import openai
import os

# ---- CONFIGURE YOUR OPENAI KEY HERE ----
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# ---- APP TITLE ----
st.title("🧠 Smart Study Planner with AI")
st.write("Get a personalized study plan with break intervals and AI help!")

# ---- USER INPUT ----
topics = st.text_area("📚 Enter your syllabus/topics (separate by comma)")
days_available = st.number_input("📅 Days available before exam", min_value=1, step=1)
hours_per_day = st.slider("⏱️ Daily study hours", 1, 12, 4)
break_interval = st.slider("☕ Break after how many minutes?", 25, 90, 50)

generate = st.button("⚡ Generate Study Plan")

# ---- GENERATE PLAN ----
def generate_study_plan(topics, days, hours):
    prompt = f"""
    Create a detailed {days}-day study schedule for the following topics: {topics}.
    Each day has {hours} hours of study time. Include Pomodoro-style breaks every {break_interval} minutes.
    Output format:
    Day X:
    - Topic 1 (1.5h)
    - Short Break (10 min)
    - Topic 2 (2h)
    ... etc.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a helpful study coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]

# ---- DISPLAY PLAN ----
if generate:
    if not topics:
        st.error("Please enter your syllabus or topics.")
    else:
        with st.spinner("Creating your study plan..."):
            try:
                plan = generate_study_plan(topics, days_available, hours_per_day)
                st.success("📋 Here's your personalized plan:")
                st.markdown(plan)
            except Exception as e:
                st.error("⚠️ Failed to generate plan. Check your OpenAI API key or internet connection.")
