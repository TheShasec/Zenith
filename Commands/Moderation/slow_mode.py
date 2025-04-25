import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
# Command to set slowmode in the current channel
@app_commands.command(name="slowmode", description="Enables slowmode for the given duration in this channel.")
@app_commands.describe(seconds="Duration of slowmode (in seconds)")
@admin_only()
async def slowmode(interaction: discord.Interaction, seconds: int):
    try:
        # Check if the given time is within the valid range
        if seconds < 0 or seconds > 21600:
            embed = discord.Embed(
                title="Invalid Duration",
                description="Please provide a value between 0 and 21600 seconds.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Set slowmode for the channel
        await interaction.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(
            title="Slowmode Successfully Set",
            description=f"Slowmode duration for this channel has been set to {seconds} seconds.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)

    except Exception as e:
        # If an error occurs, send the error message
        error_message = f"Error: {e}"
        embed = discord.Embed(
            title="An Error Occurred",
            description="An error occurred. Please try again later.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(error_message)
