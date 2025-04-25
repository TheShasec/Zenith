import discord
from discord import app_commands
from Commands.General.AI.get_ai_response_with_chatgpt import get_ai_response_with_chatgpt
from Commands.General.AI.get_ai_response_with_gemini import get_ai_response_with_gemini
import textwrap
# AI command to interact with different AI models
@app_commands.command(name="ai", description="Get a response from AI.")
@app_commands.choices(model=[
    app_commands.Choice(name="ChatGPT", value="chatgpt"),
    app_commands.Choice(name="Gemini", value="gemini")
])
@app_commands.describe(
    message="Enter the message to send to the AI model",
    model="Choose which AI model you want to use"
)
async def ai(interaction: discord.Interaction, model: app_commands.Choice[str], message: str):
    await interaction.response.defer()

    # Check if the message is empty
    if not message:
        await interaction.followup.send("Please provide a valid message.")
        return

    try:
        # Processing the message based on the selected AI model
        if model.value == "chatgpt":
            system_messages = ""
            if "+" in message:
                parts = message.split("+")
                user_message = parts[0].strip()
                if len(parts) > 1:
                    system_messages = " ".join([part.strip() for part in parts[1:]])
            else:
                user_message = message.strip()

            ai_response = await get_ai_response_with_chatgpt(user_message, system_messages)

        elif model.value == "gemini":
            ai_response = await get_ai_response_with_gemini(message.strip())

        # Sending the response in chunks if it's too long
        for chunk in textwrap.wrap(ai_response, 2000, replace_whitespace=False):
            await interaction.followup.send(chunk)

    except Exception as e:
        # Handle any exceptions that occur
        await interaction.followup.send(f"An error occurred: {str(e)}")