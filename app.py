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

st.subheader("📝 Climate Quiz")

q1 = st.radio("Which gas causes global warming?", ["Carbon Dioxide", "Oxygen"])
q2 = st.radio("Which energy is renewable?", ["Solar", "Coal"])

score = 0
if q1 == "Carbon Dioxide":
    score += 1
if q2 == "Solar":
    score += 1

st.success(f"🏆 Your Score: {score}/2")
