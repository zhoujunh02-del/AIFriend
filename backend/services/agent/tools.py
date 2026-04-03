from datetime import datetime
from langchain_core.tools import tool
from duckduckgo_search import DDGS
import numexpr
import requests 
import os  

@tool
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculator(expression):
    return str(numexpr.evaluate(expression))

@tool
def web_search(query):
    results = DDGS().text(query, max_results=3)
    return "\n".join(r["body"] for r in results)

@tool
def get_weather(city):
    key = os.getenv("OPENWEATHERMAP_API_KEY")
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": key, "units": "metric"}
    )
    data = response.json()
    return f"{data['name']}: {data['main']['temp']}°C, {data['weather'][0]['description']}"