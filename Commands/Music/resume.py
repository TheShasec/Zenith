import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
# Command to resume paused music
@app_commands.command(name="resume", description="Resumes the paused music.")
@admin_only()
async def resume(interaction: discord.Interaction):
    try:
        voice_client = interaction.guild.voice_client

        # Check if the music is paused
        if voice_client and voice_client.is_paused():
            voice_client.resume()

            embed = discord.Embed(
                title="▶️ Music Resumed",
                description="The paused music is now playing again.",
                color=discord.Color.green()
            ).set_footer(text="Enjoy your music!")
        else:
            embed = discord.Embed(
                title="❌ No Paused Music Found",
                description="There is no paused music at the moment.",
                color=discord.Color.red()
            ).set_footer(text="Use /pause to pause the music first.")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=not voice_client or not voice_client.is_paused()
        )

    except Exception as e:
        # Handle unexpected errors
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Error Resuming Music",
                description=f"An error occurred: ```{str(e)}```",
                color=discord.Color.red()
            ).set_footer(text="Try again or report this issue."),
            ephemeral=True
        )