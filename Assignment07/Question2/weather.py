import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

st.title("Weather Information App")

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        status = response.status_code
        st.write("status:", status)

        if status == 200:
            data = response.json()
            st.write(f"Weather in {city}")
            st.write(f"Temperature: {data['main']['temp']} °C")
            st.write(f"Condition: {data['weather'][0]['description'].title()}")
            st.write(f"Humidity: {data['main']['humidity']}%")
            st.write(f"Wind Speed: {data['wind']['speed']} m/s")
        else:
            st.write("City not found or invalid API key")
