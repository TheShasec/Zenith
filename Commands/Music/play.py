import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
from Commands.Music.music import YTDLSource

# Command to play music from a YouTube URL
@app_commands.command(name="play", description="Plays music from a YouTube URL.")
@app_commands.describe(url="YouTube URL of the music")
@admin_only()
async def play(interaction: discord.Interaction, url: str):
    try:
        # If the bot is not connected to a voice channel
        if not interaction.guild.voice_client:
            # If the user is in a voice channel, connect the bot
            if interaction.user.voice:
                await interaction.user.voice.channel.connect()
            else:
                # If user is not in a voice channel, send error embed
                embed = discord.Embed(
                    title="❌ You Are Not in a Voice Channel!",
                    description="Please join a voice channel first.",
                    color=discord.Color.red()
                ).set_footer(text="Join a voice channel and try again.")

                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        # Notify the user that the music is being processed
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🎵 Preparing Music...",
                description=f"Link: [Click Here]({url})",
                color=discord.Color.blue()
            ).set_footer(text="Please wait while the music is loading...")
        )

        # Get the active voice client
        voice_client = interaction.guild.voice_client

        # Try to create a player from the YouTube URL
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

        # Play the audio and handle any playback errors
        voice_client.play(player, after=lambda e: print(f"[Playback Error] {e}") if e else None)

        # Send a follow-up message with the now playing information
        await interaction.followup.send(
            embed=discord.Embed(
                title="🎶 Now Playing",
                description=f"**{player.title}**\n\nLink: [Click Here]({url})",
                color=discord.Color.green()
            ).set_footer(text="Enjoy your music!")
        )

    except Exception as e:
        # Handle any unexpected errors during music playback
        await interaction.followup.send(
            embed=discord.Embed(
                title="⚠️ Playback Error",
                description=f"Error message: ```{str(e)}```",
                color=discord.Color.red()
            ).set_footer(text="Please try using a different link.")
        )
