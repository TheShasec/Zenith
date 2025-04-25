import discord
from discord import app_commands
from Database.rankDB import get_user_level

# Level command to show the user's level and XP
@app_commands.command(name="level", description="Displays your level and XP.")
async def level(interaction: discord.Interaction):
    """Command to show user's level and XP."""
    user_id = interaction.user.id
    guild_id = interaction.guild.id  

    # Get user's level and XP from the database
    user_data = get_user_level(user_id, guild_id)

    level = user_data["level"]
    xp = user_data["xp"]
    target_xp = 20 + (level * 50)  # XP required to level up

    # Create an embed to show level info
    embed = discord.Embed(
        title=f"{interaction.user.name} - Level Information",
        description=f"**Level**: {level}\n**XP**: {xp}/{target_xp}",
        color=discord.Color.green()
    )
    embed.set_footer(text="Level system | Powered by the bot.")

    # Send the level info as a response
    await interaction.response.send_message(embed=embed)
