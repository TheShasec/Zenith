import discord
from discord import app_commands
import asyncio
import datetime

# Remind Command 
@app_commands.command(name="remind", description="Set a reminder with specified time unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Seconds", value="seconds"),
    app_commands.Choice(name="Minutes", value="minutes"),
    app_commands.Choice(name="Hours", value="hours"),
    app_commands.Choice(name="Days", value="days")
])
async def remind(interaction: discord.Interaction, time: int, unit: str, reminder: str):
    # Time conversion dictionary
    time_conversion = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
    
    # Check if the time is valid
    if time <= 0:
        await interaction.response.send_message("Please specify a positive time value.", ephemeral=True)
        return
        
    # Check if the reminder is too long
    if len(reminder) > 1000:
        await interaction.response.send_message(
            "Your reminder message is too long. Please keep it under 1000 characters.",
            ephemeral=True
        )
        return
    
    try:
        # Calculate seconds
        seconds = time * time_conversion[unit]
        
        # Check if the time is too long
        if seconds > 2592000: # 30 days
            await interaction.response.send_message(
                "Reminder time is too long. Maximum is 30 days.",
                ephemeral=True
            )
            return
            
        # Calculate when the reminder will trigger
        reminder_time = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        
        # Create embed for confirmation
        embed = discord.Embed(
            title="⏰ Reminder Set",
            description=f"I'll remind you about: **{reminder}**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Time", value=f"{time} {unit}")
        embed.add_field(name="Reminder will trigger", value=f"<t:{int(reminder_time.timestamp())}:R>")
        
        # Send confirmation message 
        await interaction.response.send_message(embed=embed,ephemeral=True)
        
        # Get the original message to delete it later
        confirmation_message = await interaction.original_response()
        
        # Start a task to delete the confirmation message after 1 minute
        asyncio.create_task(delete_after_delay(confirmation_message, 60))
        
        # Store original channel and user for later use
        channel = interaction.channel
        user = interaction.user
        
        # Wait for the specified time
        await asyncio.sleep(seconds)
        
        # Create reminder embed
        reminder_embed = discord.Embed(
            title="⏰ Reminder",
            description=reminder,
            color=discord.Color.green()
        )
        reminder_embed.set_footer(text=f"Reminder set {time} {unit} ago")
        
        # Try to DM the user
        try:
            await user.send(
                content=f"Hey {user.mention}, here's your reminder!",
                embed=reminder_embed
            )
        except:
            pass # If DM fails, we'll still try to send to the channel
            
        # Send to the original channel
        try:
            # Send message and store the message object
            reminder_message = await channel.send(
                content=f"{user.mention}, here's your reminder!",
                embed=reminder_embed
            )
            
            # Delete the reminder message after 1 minute
            asyncio.create_task(delete_after_delay(reminder_message, 60))
                
        except:
            # If the channel doesn't exist, we've already tried DMing
            pass
            
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

# Helper function to delete a message after a delay
async def delete_after_delay(message, delay_seconds):
    await asyncio.sleep(delay_seconds)
    try:
        await message.delete()
    except:
        # If deletion fails, continue silently
        pass