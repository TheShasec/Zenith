import discord
from discord import app_commands
import json
import datetime
import os

@app_commands.command(name="help", description="Provides information about the bot's commands.")
async def help(interaction: discord.Interaction):
    try:
        # Specify the correct file path to the commands JSON file
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir,  "..", ".."))  

        file_path = os.path.join(project_root, "Database", "commands.json")


        
        # Open and read the JSON file containing command definitions
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create the main embed message for help
        embed = discord.Embed(
            title="📚 Bot Command Help",
            description="Here's a quick overview of available commands. For detailed information visit our website.",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        # Lists to categorize the commands
        game_commands = []
        music_commands = []
        moderation_commands = []
        general_commands = []

        # Categorizing commands based on their names
        for cmd in data["commands"]:
            if cmd in ["level", "rockpaperscissors", "roll_dice"]:
                game_commands.append(cmd)
            elif cmd in ["join", "leave", "pause", "play", "resume", "stop"]:
                music_commands.append(cmd)
            elif cmd in ["slowmode", "clear"]:
                moderation_commands.append(cmd)
            else:
                general_commands.append(cmd)

        # Add game commands - only display command names
        if game_commands:
            game_text = "".join(f"`/{cmd}` " for cmd in game_commands)
            embed.add_field(name="🎮 Game Commands", value=game_text, inline=False)

        # Add music commands - only display command names
        if music_commands:
            music_text = "".join(f"`/{cmd}` " for cmd in music_commands)
            embed.add_field(name="🎵 Music Commands", value=music_text, inline=False)

        # Add utility/general commands - only display command names
        if general_commands:
            utility_text = "".join(f"`/{cmd}` " for cmd in general_commands)
            embed.add_field(name="🛠️ Utility Commands", value=utility_text, inline=False)

        # Add Moderation commands - only display command names
        if moderation_commands:
            moderation_text = "".join(f"`/{cmd}` " for cmd in moderation_commands)
            embed.add_field(name="ℹ️ Moderation Commands", value=moderation_text, inline=False)

        
        # Link to the website for detailed documentation
        embed.add_field(
            name="📋 Detailed Documentation", 
            value="For command details and examples, visit [our website](https://zenithsite.vercel.app/).", 
            inline=False
        )
        
        # Footer with bot developer credit
        embed.set_footer(text="Developed by The Shasec | Type /help to see this message again")
        
        # Send the embed as a response
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        # Exception handling: if any error occurs, display an error message
        print(f"Error in help command: {e}")
        error_embed = discord.Embed(
            title="❌ An error occurred!",
            description=f"Unable to provide help information:\n```{str(e)}```\nPlease try again later or contact the bot developer.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed)
