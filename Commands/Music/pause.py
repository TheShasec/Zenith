import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
# Command to pause the currently playing music
@app_commands.command(name="pause", description="Pauses the currently playing music.")
@admin_only()
async def pause(interaction: discord.Interaction):
    try:
        voice_client = interaction.guild.voice_client

        # Check if music is currently playing
        if voice_client and voice_client.is_playing():
            voice_client.pause()

            embed = discord.Embed(
                title="⏸️ Music Paused",
                description="The currently playing music has been successfully paused.",
                color=discord.Color.orange()
            ).set_footer(text="Use /resume to continue playing.")
        else:
            embed = discord.Embed(
                title="❌ No Music Found!",
                description="There is no music playing right now.",
                color=discord.Color.red()
            ).set_footer(text="Start playing music first before pausing.")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=not voice_client or not voice_client.is_playing()
        )

    except Exception as e:
        # Handle unexpected errors
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Error Pausing Music",
                description=f"An error occurred: ```{str(e)}```",
                color=discord.Color.red()
            ).set_footer(text="Try again or report this issue."),
            ephemeral=True
        )
