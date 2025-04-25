from collections import defaultdict
import time
import discord
import datetime
from discord.utils import utcnow

# Data structure for user messages
user_messages = defaultdict(list)

# Function to block spam
async def mute_spam(message):
    user_id = message.author.id
    current_time = time.time()

    # Add the user's message time
    user_messages[user_id].append(current_time)

    # Check if the user sent more than 5 messages in the last 5 seconds
    recent_messages = [t for t in user_messages[user_id] if current_time - t < 5]

    # If more than 5 messages in 5 seconds, mute the user
    if len(recent_messages) > 5:
        await message.channel.send(f"{message.author.mention}, please avoid spamming! ⛔ **You have been muted for 1 minute.**")

        # Mute the user for 1 minute (timeout)
        try:
            # Use utcnow() for an aware datetime (UTC)
            mute_end_time = utcnow() + datetime.timedelta(minutes=1)
            await message.author.timeout(mute_end_time, reason="Muted for spamming.")
        except Exception as e:
            print(f"Mute operation failed: {e}")

    # Keep only the most recent messages
    user_messages[user_id] = recent_messages
