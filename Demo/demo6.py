import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("WEATHER_API_KEY")

city=input("Enter city name: ")
url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response=requests.get(url)
status=response.status_code
print("status:", status)
if response.status_code==200:
    data=response.json()
    print(f"Weather in {city}:")
    print(f"Temperature: {data['main']['temp']} °C")
    print(f"Condition: {data['weather'][0]['description'].title()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")
else:
    print("City not found or invalid API key")

if __name__ == "__main__":
    pass