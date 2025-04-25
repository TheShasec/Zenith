import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only

# Command to connect the bot to the user's voice channel
@app_commands.command(name="join", description="Invites the bot to a voice channel.")
@admin_only()
async def join(interaction: discord.Interaction):
    try:
        # Check if the user is currently in a voice channel
        if interaction.user.voice:
            # Get the voice channel the user is connected to
            channel = interaction.user.voice.channel

            # Connect the bot to the same voice channel
            await channel.connect()

            # Create a success embed message
            embed = discord.Embed(
                title="✅ Joined Voice Channel!",
                description=f"Successfully connected to **{channel.name}**.",
                color=discord.Color.green()
            ).set_footer(text="You can now use music commands!")

            # Send the embed as a response to the interaction
            await interaction.response.send_message(embed=embed)

        else:
            # If the user is not in any voice channel, send an error message
            embed = discord.Embed(
                title="❌ You Are Not in a Voice Channel!",
                description="Please join a voice channel first.",
                color=discord.Color.red()
            ).set_footer(text="Try again after joining a voice channel.")

            await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        # Handle unexpected errors during the connection process
        print(f"[Join Command Error] {e}")
        await interaction.response.send_message(
            "An error occurred while trying to join the voice channel.",
            ephemeral=True
        )
