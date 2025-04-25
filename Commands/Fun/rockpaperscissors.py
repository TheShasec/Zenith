import random
import discord
from discord import app_commands
# Command to play the "Rock, Paper, Scissors" game
@app_commands.command(name="rockpaperscissors", description="Play the Rock, Paper, Scissors game!")
async def rockpaperscissors(interaction: discord.Interaction, choice: str):
    try:
        # Valid choices for the game
        choices = ["rock", "paper", "scissors"]
        user_choice = choice.lower()

        # Check if the user's choice is valid
        if user_choice not in choices:
            await interaction.response.send_message("❌ Invalid choice! Please write `rock`, `paper`, or `scissors`.")
            return

        # Bot's choice is randomly selected
        bot_choice = random.choice(choices)

        # Determine the game result
        result, description = determine_game_result(user_choice, bot_choice)

        # Embed for game result
        embed = discord.Embed(
            title="Rock, Paper, Scissors Results",
            description=description,
            color=discord.Color.green() if result == "Congratulations, you won!" else discord.Color.red()
        )
        embed.add_field(name="Result", value=result, inline=True)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        # If an error occurs during the game, send the error message
        error_message = f"[RockPaperScissors Error] {e}"
        embed = discord.Embed(
            title="An Error Occurred",
            description="An error occurred while processing your game. Please try again.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(error_message)

# Helper function to determine the result of the Rock, Paper, Scissors game
def determine_game_result(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a Tie!", f"Your choice: **{user_choice}**\nBot's choice: **{bot_choice}**"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        return "Congratulations, you won!", f"Your choice: **{user_choice}**\nBot's choice: **{bot_choice}**"
    else:
        return "Sorry, you lost!", f"Your choice: **{user_choice}**\nBot's choice: **{bot_choice}**"

