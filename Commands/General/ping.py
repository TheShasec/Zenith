import discord
from discord import app_commands
import datetime
@app_commands.command(name="ping", description="Measures the bot's latency.")
async def ping(interaction: discord.Interaction):
    try:
        latency = round(interaction.client.latency * 1000)  # Convert latency from seconds to milliseconds

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"🔹 **Bot Latency:** {latency}ms",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        # Error handling: catch any exceptions and show an error message
        print(f"Error: {e}")
        embed = discord.Embed(
            title="An error occurred!",
            description="Unable to check latency, please try again.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

