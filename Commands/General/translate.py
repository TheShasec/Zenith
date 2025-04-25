import discord
from discord import app_commands
from googletrans import Translator


# Initialize the Translator object
translator = Translator()

# Translation function
async def translate_text(text: str, dest: str = "en") -> str:
    try:
        # Perform the translation
        result = await translator.translate(text, dest=dest)
        return result.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Discord bot command
@app_commands.command(name="translate", description="Translates text to another language.")
@app_commands.describe(text="The text to be translated", language="The target language code (en, tr, de...)")
async def translate(interaction: discord.Interaction, text: str, language: str):
    await interaction.response.defer(thinking=True)  # Sends a 'thinking' message while processing the translation
    
    # Perform the translation
    translated = await translate_text(text, dest=language)
    
    # Send the result
    await interaction.followup.send(f"**Translation ({language}):** {translated}")
