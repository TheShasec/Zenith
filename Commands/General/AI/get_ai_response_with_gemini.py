import aiohttp
from openai import OpenAI
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Function to get AI response from Google's Gemini model
async def get_ai_response_with_gemini(message):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{message}"
        )
        return response.text

    except Exception as e:
        return f"An error occurred while getting a response from Gemini: {str(e)}"
