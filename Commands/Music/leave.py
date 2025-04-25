import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only

# Command to disconnect the bot from the voice channel
@app_commands.command(name="leave", description="Disconnects the bot from the voice channel.")
@admin_only()
async def leave(interaction: discord.Interaction):
    try:
        # Get the current voice client (if the bot is connected)
        voice_client = interaction.guild.voice_client

        if voice_client:
            # Disconnect the bot from the voice channel
            await voice_client.disconnect()

            # Create a confirmation embed message
            embed = discord.Embed(
                title="📤 Left Voice Channel!",
                description="Successfully disconnected from the voice channel.",
                color=discord.Color.orange()
            ).set_footer(text="Use /join to connect again!")

            await interaction.response.send_message(embed=embed)

        else:
            # If the bot is not in any voice channel, inform the user
            embed = discord.Embed(
                title="❌ Not Connected!",
                description="I am not currently in any voice channel.",
                color=discord.Color.red()
            ).set_footer(text="Use the /join command first to connect to a channel.")

            await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        # Handle unexpected errors during disconnection
        print(f"[Leave Command Error] {e}")
        await interaction.response.send_message(
            "An error occurred while trying to disconnect from the voice channel.",
            ephemeral=True
        )