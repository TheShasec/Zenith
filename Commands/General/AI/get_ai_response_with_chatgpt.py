import aiohttp
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API client with a custom base URL
base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=OPENAI_API_KEY, base_url=base_url)

# Function to get AI response from ChatGPT (gpt-4o-mini)
async def get_ai_response_with_chatgpt(user_message, system_messages):
    try:
        user_message_obj = {"role": "user", "content": user_message}

        # Prepare messages list depending on whether system prompt is provided
        if system_messages:
            completion = api.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_messages},
                    user_message_obj,
                    {"role": "system", "content": "Please provide responses with a maximum of 256 tokens."}
                ],
                temperature=0.7,
                max_tokens=256,
            )
        else:
            completion = api.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Please provide responses with a maximum of 256 tokens."},
                    user_message_obj
                ],
                temperature=0.7,
                max_tokens=256,
            )

        # Extract the content from the first choice
        response = completion.choices[0].message.content
        return response

    except Exception as e:
        # In case of an error, return a friendly fallback message
        return f"An error occurred while getting a response from ChatGPT: {str(e)}"