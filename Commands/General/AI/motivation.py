import discord
from discord import app_commands
from Commands.General.AI.get_ai_response_with_chatgpt import get_ai_response_with_chatgpt

# Motivation command
@app_commands.command(name="motivation", description="Sends a motivational quote.")
async def motivation(interaction: discord.Interaction):
    # Get a motivational quote from the AI
    ai_response = await get_ai_response_with_chatgpt("Write a motivational sentence.", "")
    await interaction.response.send_message(ai_response)
