import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
# Command to stop the currently playing music
@app_commands.command(name="stop", description="Stops the currently playing music.")
@admin_only()
async def stop(interaction: discord.Interaction):
    try:
        # Get the active voice client for the guild
        voice_client = interaction.guild.voice_client
        # If music is playing, stop it
        if voice_client and voice_client.is_playing():
            voice_client.stop()

            embed = discord.Embed(
                title="⏹️ Music Stopped",
                description="The currently playing music has been stopped successfully.",
                color=discord.Color.orange()
            ).set_footer(text="Use /play to start playing music again.")
        else:
            # If no music is playing, send an informative message
            embed = discord.Embed(
                title="❌ No Music Playing!",
                description="There is no music currently playing.",
                color=discord.Color.red()
            ).set_footer(text="You need to start music first using the /play command.")

        # Send response (ephemeral if nothing is playing)
        await interaction.response.send_message(embed=embed, ephemeral=not voice_client or not voice_client.is_playing())

    except Exception as e:
        # Handle any unexpected errors during stopping music
        print(f"[Stop Command Error] {e}")
        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Error While Stopping",
                description=f"Something went wrong: ```{str(e)}```",
                color=discord.Color.red()
            ).set_footer(text="Try again or report the issue."),
            ephemeral=True
        )