import os
import time
import json
import random
import sqlite3
import datetime
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from collections import defaultdict
import aiohttp
import textwrap
from discord.ext import tasks
from typing import List
import asyncio
from Commands.Moderation.admin_only import admin_only
from Database.db import (
    add_user_to_database,
    get_db,
    setup_database
)
from Database.rankDB import (
    add_xp,
    create_rank_db
)

from Commands.General.serverinfo import serverinfo
from Commands.General.ping import ping
from Commands.General.help import help
from Commands.Music.join import join
from Commands.Music.leave import leave
from Commands.Music.pause import pause
from Commands.Music.play import play
from Commands.Music.resume import resume
from Commands.Music.stop import stop
from Commands.Fun.rockpaperscissors import rockpaperscissors
from Commands.Fun.roll import roll_dice
from Commands.Moderation.slow_mode import slowmode
from Commands.Moderation.mute_spam import mute_spam
from Commands.General.Weather.weather import weather
from Commands.General.AI.ai import ai
from Commands.General.AI.motivation import motivation
from Commands.General.translate import translate
from Commands.Fun.level import level
from Commands.General.wiki import wikipedia
from Commands.General.poll import create_poll
from Commands.General.currency import currency_command
from Commands.General.crypto import crypto_command
from Commands.General.crypto import fetch_coins
from Commands.Moderation.clear import clear
from Commands.General.remind import remind
from Commands.Moderation.profanity_detector import check_profanity
# Load environment variables
load_dotenv()
DC_API_KEY = os.getenv("DC_API_KEY")

# Discord bot permissions
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)


def setup_music():
    bot.tree.add_command(join)
    bot.tree.add_command(leave)
    bot.tree.add_command(pause)
    bot.tree.add_command(play)
    bot.tree.add_command(resume)
    bot.tree.add_command(stop)
def setup_moderation():
    bot.tree.add_command(slowmode)
    bot.tree.add_command(clear)
def setup_general():
    bot.tree.add_command(weather)
    bot.tree.add_command(serverinfo)
    bot.tree.add_command(help)
    bot.tree.add_command(ping)
    bot.tree.add_command(ai)
    bot.tree.add_command(motivation)
    bot.tree.add_command(translate)
    bot.tree.add_command(wikipedia)
    bot.tree.add_command(create_poll)
    bot.tree.add_command(currency_command)
    bot.tree.add_command(crypto_command)
    bot.tree.add_command(remind)
def setup_fun():
    bot.tree.add_command(roll_dice)
    bot.tree.add_command(rockpaperscissors)
    bot.tree.add_command(level)
def add_command():
    setup_music()
    setup_moderation()
    setup_general()
    setup_fun()

# Global error handler for command errors (e.g., permission check failure)
@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error: Exception):
    # Check if the interaction already has a response
    if interaction.response.is_done():
        return  # Don't respond again if already responded
    
    # Handle CheckFailure error
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        embed = discord.Embed(
            title="Permission Error 🚫",
            description="You must have **Administrator** permission to use this command!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        # Handle other exceptions
        embed = discord.Embed(
            title="An Unexpected Error Occurred",
            description="Something went wrong. Please try again later.",
            color=discord.Color.red()
        )
        print(error)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Utility function to get a database connection and cursor
def get_db_cursor():
    conn = get_db()  # Assumes get_db() is defined elsewhere
    cursor = conn.cursor()
    return conn, cursor

# Adds a user to the database if they do not already exist
async def add_user_if_not_exists(member):
    try:
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ? AND guild_id = ?", (member.id, member.guild.id))
        if not cursor.fetchone():
            add_user_to_database(member)  # Assumes this function is defined elsewhere
        conn.close()
    except Exception as e:
        # Send the error message to Discord (to the member or a specific channel)
        channel = member.guild.text_channels[0]  # First text channel of the server
        await channel.send(f"[Database Error] Failed to check/add user: {e}")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    try:
        print(f'{bot.user} has connected to the server!')
        add_command()
        # Initialize the main database and ranking system
        setup_database()      # Assumes defined elsewhere
        create_rank_db()      # Assumes defined elsewhere
        # Sync slash commands per guild and ensure all members are tracked in DB
        for guild in bot.guilds:
            await bot.tree.sync(guild=discord.Object(id=guild.id))
            for member in guild.members:
                if not member.bot:
                    await add_user_if_not_exists(member)

        # Global sync (optional)
        await bot.tree.sync()

        # Fetch coin data (presumably for some currency system)
        await fetch_coins()  # Assumes defined elsewhere

    except Exception as e:
        # Send the error message to the first channel of the guild
        for guild in bot.guilds:
            channel = guild.text_channels[0]  # You can change the channel here
            await channel.send(f"[on_ready Error] {e}")

# Event triggered when a new member joins the server
@bot.event
async def on_member_join(member):
    try:
        if not member.bot:
            # Add user to the database if they don't exist
            await add_user_if_not_exists(member)

        # Get the system channel for the guild
        channel = member.guild.system_channel  

        if channel:
            # Create the welcome embed message
            embed = discord.Embed(
                title="🎉 Welcome!",
                description=f"Hello {member.mention}, welcome to our server! 🚀\n\nWe hope you have a fantastic time here!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text=f"You joined the {member.guild.name} family!", icon_url=member.guild.icon.url if member.guild.icon else None)

            # Send the welcome message to the system channel
            await channel.send(embed=embed)

    except Exception as e:
        # If an error occurs, send the error message to the first text channel
        error_message = f"[Member Join Error] {e}"
        for guild in bot.guilds:
            channel = guild.text_channels[0]  # You can change this to a specific channel if needed
            await channel.send(error_message)

# Event triggered when a member leaves the server
@bot.event
async def on_member_remove(member):
    try:
        if not member.bot:
            # Remove the user from the database when they leave
            conn, cursor = get_db_cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ? AND guild_id = ?",
                           (member.id, member.guild.id))
            conn.commit()
            conn.close()
    except Exception as e:
        # If an error occurs, send the error message to the first text channel
        error_message = f"[Member Remove Error] {e}"
        for guild in bot.guilds:
            channel = guild.text_channels[0]  # You can change this to a specific channel if needed
            await channel.send(error_message)

# Event triggered when a member updates their details (e.g. username change)
@bot.event
async def on_member_update(before, after):
    try:
        # Check if the member's username has changed
        if before.name != after.name:
            # Open a database connection and get cursor
            conn, cursor = get_db_cursor()

            # Update the username in the database
            cursor.execute("UPDATE users SET username = ? WHERE user_id = ? AND guild_id = ?",
                           (after.name, after.id, after.guild.id))
            
            # Save changes and close connection
            conn.commit()
            conn.close()
    except Exception as e:
        # If an error occurs, send the error message to the first text channel of each guild
        for guild in bot.guilds:
            channel = guild.text_channels[0]  # You can choose a specific channel if preferred
            await channel.send(f"[Member Update Error] {e}")

@bot.event
async def on_message(message):
    """Adds XP when a message is sent."""
    # Ignore messages from bots
    if message.author.bot:
        return  # Bot messages are not considered

    # Add 10 XP for each message sent
    level, new_xp = add_xp(message.author.id, message.guild.id, 10)

    
    # If the user leveled up, send a congratulatory message
    if new_xp == 0:
        embed = discord.Embed(
            title=f"Congratulations, {message.author.name}!",
            description=f"**You have successfully reached level {level}!**",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Level system | Powered by the bot.")
        await message.channel.send(embed=embed)

    # Call the function to mute spam
    await mute_spam(message=message)

    # Check message content using our function
    is_toxic = await check_profanity(message.content)
    # If profanity is detected
    if is_toxic:
        # Delete the message
        await message.delete()
        embed = discord.Embed()
        embed.title = "⚠️ Inappropriate Content Detected"
        embed.description = f"**{message.author.name}**, your message contains inappropriate language."
        embed.color = discord.Color.red()
        embed.set_footer(text="This message violates our community guidelines.")
        embed.timestamp = discord.utils.utcnow()  
        
        # Send warning to the user
        await message.channel.send(
            embed=embed
        )
        return
    # Process commands as usual
    await bot.process_commands(message)

bot.run(DC_API_KEY)
