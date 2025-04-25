import aiohttp
import json
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Hugging Face API token 
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

async def check_profanity(content, threshold=0.5):
    # API URL for the toxicity model
    api_url = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
    
    # Headers with authorization
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json={"inputs": content}) as response:
                if response.status != 200:
                    print(f"API error: {response.status}")
                    return False
                    
                result = await response.json()
                
                # Check for toxicity in results
                for item in result[0]:
                    if item["label"] == "toxic" and item["score"] > threshold:
                        return True
                        
                return False
    except Exception as e:
        print(f"Error in profanity detection API call: {e}")
        return False