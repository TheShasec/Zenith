import aiohttp
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Function to fetch geocoding (latitude & longitude) for a given city and country code
async def get_geocoding(city, limit=1):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city}",
        "limit": limit,
        "appid": WEATHER_API_KEY
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()  # Raises an error if response status is not 200
                geocoding_data = await response.json()
                return geocoding_data
    except Exception as e:
        return {"error": f"An error occurred while fetching geocoding data: {str(e)}"}