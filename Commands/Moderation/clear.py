import discord
from discord import app_commands
import datetime

# Clear Command
@app_commands.command(name="clear", description="Delete a specified number of messages")
async def clear(interaction: discord.Interaction, amount: int = 5):
    # Check if the user has permission to manage messages
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    
    # Check if the amount is valid
    if amount <= 0:
        await interaction.response.send_message("Please specify a positive number of messages to delete.", ephemeral=True)
        return
    if amount > 100:
        await interaction.response.send_message("You can only delete up to 100 messages at once.", ephemeral=True)
        return
    
    try:
        # Defer the response to avoid timeout
        await interaction.response.defer(ephemeral=True)
        
        # Get messages to delete
        messages = []
        async for message in interaction.channel.history(limit=amount):
            messages.append(message)
        
        # Delete the messages
        if not messages:
            await interaction.followup.send("No messages found to delete.", ephemeral=True)
            return
        
        if len(messages) == 1:
            await messages[0].delete()
            deleted_count = 1
        else:
            # Check message age - Discord API only allows bulk deletion of messages <14 days old
            now = discord.utils.utcnow()
            two_weeks_ago = now - datetime.timedelta(days=14)
            
            # Split messages into two groups - newer than 14 days and older than 14 days
            recent_messages = [msg for msg in messages if msg.created_at > two_weeks_ago]
            old_messages = [msg for msg in messages if msg.created_at <= two_weeks_ago]
            
            # Bulk delete recent messages
            deleted_count = 0
            if recent_messages:
                await interaction.channel.delete_messages(recent_messages)
                deleted_count += len(recent_messages)
            
            # Delete old messages one by one
            for message in old_messages:
                try:
                    await message.delete()
                    deleted_count += 1
                except Exception:
                    continue
        
        await interaction.followup.send(f"Successfully deleted {deleted_count} messages.", ephemeral=True)
    
    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to delete messages in this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.followup.send(f"Failed to delete messages: {str(e)}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)