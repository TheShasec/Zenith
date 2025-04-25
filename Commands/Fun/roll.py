import random
import discord
from discord import app_commands


@app_commands.command(name="roll_dice", description="Roll a dice and show the result!")
async def roll_dice(interaction: discord.Interaction, guess: int):
    try:
        # Roll a dice and get a random number between 1 and 6
        roll_result = random.randint(1, 6)
        # Check if the user's guess is valid (between 1 and 6)
        if guess > 6 or guess < 1:
            embed = discord.Embed(
                title="Error!",
                description="Please enter a number between 1 and 6.",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            return

        # If the user's guess is correct
        if guess == roll_result:
            embed = discord.Embed(
                title="🎲 Dice Roll!",
                description=f"The dice was rolled! Result: **{roll_result}**\nCongratulations, you guessed correctly!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="🎲 Dice Roll!",
                description=f"The dice was rolled! Result: **{roll_result}**\nSorry, you guessed wrong.",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        # Error handling: catch any exceptions and show an error message
        print(f"Error: {e}")
        embed = discord.Embed(
            title="An error occurred!",
            description="Something went wrong, please try again.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)