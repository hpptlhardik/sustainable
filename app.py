from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green, black
import io
from datetime import date
import time
import random
import streamlit as st
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Sustainable Weather AI Chatbot")
st.title("🌍 Sustainable Weather AI Chatbot")

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    if data.get("cod") != 200:
        return None
    return data

city = st.text_input("Enter City Name")

if st.button("Get Weather"):
    data = get_weather(city)
    if data:
        st.success(f"🌡 Temp: {data['main']['temp']}°C")
        st.success(f"💧 Humidity: {data['main']['humidity']}%")
        st.success(f"🌦 Condition: {data['weather'][0]['description']}")
    else:
        st.error("City not found")

st.subheader("🔮 Temperature Prediction")

humidity = st.slider("Humidity (%)", 30, 90, 60)
pressure = st.slider("Pressure (hPa)", 1000, 1025, 1012)

df = pd.DataFrame({
    "humidity": [40, 50, 60, 70, 80],
    "pressure": [1010, 1012, 1013, 1011, 1009],
    "temp": [22, 25, 28, 31, 34]
})

model = LinearRegression()
model.fit(df[["humidity", "pressure"]], df["temp"])

if st.button("Predict Temperature"):
    pred = model.predict([[humidity, pressure]])
    st.success(f"Predicted Temperature: {pred[0]:.2f} °C")
 

# Initialize timer
if "quiz_start_time" not in st.session_state:
    st.session_state.quiz_start_time = time.time()

TIME_LIMIT = 60  # seconds
elapsed = int(time.time() - st.session_state.quiz_start_time)
time_left = TIME_LIMIT - elapsed

timer_placeholder = st.empty()
timer_placeholder.info(f"⏱️ Time left: {time_left} seconds")

# Stop quiz when time is over
if time_left <= 0:
    st.warning("⏰ Time is up! Quiz submitted.")
    st.session_state.time_up = True
else:
    st.session_state.time_up = False

st.subheader("📝 Climate Quiz")

# Quiz questions
q1 = st.radio(
    "Which gas causes global warming?",
    ["Carbon Dioxide", "Oxygen"],
    key="q1"
)

q2 = st.radio(
    "Which energy is renewable?",
    ["Solar", "Coal"],
    key="q2"
)

# Calculate score
score = 0
if q1 == "Carbon Dioxide":
    score += 1
if q2 == "Solar":
    score += 1

# Show result
if st.session_state.time_up or st.button("Submit Quiz"):
    st.success(f"✅ Your score: {score}/2")
    st.session_state.quiz_completed = True
    st.stop()

# Auto refresh every second
time.sleep(1)
st.experimental_rerun()
all_questions = [
    ("Which gas causes global warming?", 
     ["Carbon Dioxide", "Oxygen", "Nitrogen"], 
     "Carbon Dioxide"),

    ("Which energy source is renewable?", 
     ["Solar", "Coal", "Oil"], 
     "Solar"),

    ("Which activity increases carbon footprint?", 
     ["Using public transport", "Burning fossil fuels", "Planting trees"], 
     "Burning fossil fuels"),

    ("What causes climate change?", 
     ["Greenhouse gases", "Rainfall", "Wind"], 
     "Greenhouse gases"),

    ("Which is a sustainable practice?", 
     ["Deforestation", "Recycling", "Plastic burning"], 
     "Recycling")
]

random.shuffle(all_questions)
quiz_questions = all_questions[:3]   # show 3 random questions
import os

LEADERBOARD_FILE = "leaderboard.csv"

if not os.path.exists(LEADERBOARD_FILE):
    df = pd.DataFrame(columns=["Name", "Score"])
    df.to_csv(LEADERBOARD_FILE, index=False)

name = st.text_input("Enter your name for leaderboard")

if st.button("Submit Score"):
    df = pd.read_csv(LEADERBOARD_FILE)
    df = df.append({"Name": name, "Score": score}, ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)
    st.success("Score saved!")
st.subheader("🏆 Leaderboard")
st.table(pd.read_csv(LEADERBOARD_FILE).sort_values(by="Score", ascending=False))
st.subheader("🤖 Ask the Sustainable Weather Bot")

user_question = st.text_input("Ask a question about climate or weather")

if user_question:
    if "climate" in user_question.lower():
        st.write("Climate refers to long-term weather patterns.")
    elif "sustainable" in user_question.lower():
        st.write("Sustainability means meeting needs without harming future generations.")
    elif "global warming" in user_question.lower():
        st.write("Global warming is caused by greenhouse gases trapping heat.")
    else:
        st.write("I can answer questions on weather, climate change, and sustainability.")



