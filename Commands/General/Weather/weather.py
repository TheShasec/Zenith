import aiohttp
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from Commands.General.Weather.get_geocoding import get_geocoding
from Commands.General.Weather.get_weather import get_weather
# Load environment variables from the .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Asynchronous error handling function
async def handle_error(interaction, error):
    await interaction.response.send_message(f"An error occurred: {str(error)}")
    
# Weather command
@app_commands.command(name="weather", description="Displays the weather information of a city.")
async def weather(interaction: discord.Interaction, city: str):
    if not city:
        await interaction.response.send_message("Please provide a city name.")
        return
    try:
        geo = await get_geocoding(city)
        lat, lon = geo[0]["lat"], geo[0]["lon"]
        weather_data = await get_weather(lat, lon)

        weather_message = f"""
        ☁️ Weather: {weather_data['weather'][0]['description']}
        🌡️ Temperature: {weather_data['main']['temp']}°C (Feels like: {weather_data['main']['feels_like']}°C)
        📉 Minimum: {weather_data['main']['temp_min']}°C
        📈 Maximum: {weather_data['main']['temp_max']}°C
        💧 Humidity: %{weather_data['main']['humidity']}
        🌬️ Wind speed: {weather_data['wind']['speed']} m/s
        """
        await interaction.response.send_message(weather_message)
    except Exception as e:
        await handle_error(interaction, e)
