from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
load_dotenv()
    
app = FastAPI()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {"error": data.get("message", "Failed to fetch weather")}

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            }
        ]
    }

@app.post("/tools/get_weather")
def weather_tool(payload: dict):
    city = payload.get("city")
    return get_weather(city)