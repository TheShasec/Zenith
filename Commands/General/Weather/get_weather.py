import aiohttp
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Function to fetch current weather data using latitude and longitude
async def get_weather(lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # Temperature in Celsius
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                weather_data = await response.json()
                return weather_data
    except Exception as e:
        return {"error": f"An error occurred while fetching weather data: {str(e)}"}
