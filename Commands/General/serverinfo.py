import discord
from discord import app_commands
import datetime
@app_commands.command(name="serverinfo", description="Displays detailed information about the server")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    
    # Server creation date
    created_at = guild.created_at.strftime("%d %B %Y, %H:%M")
    
    # User statistics
    total_members = guild.member_count
    humans = len([m for m in guild.members if not m.bot])
    bots = len([m for m in guild.members if m.bot])
    
  
    # Channel statistics
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    total_channels = text_channels + voice_channels
    
    # Role count
    role_count = len(guild.roles) - 1  # Not counting @everyone role
    
    
    
    # Create embed
    embed = discord.Embed(
        title=f"{guild.name} Server Information",
        description=f"ID: {guild.id}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    # Set server icon as thumbnail if available
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    # Add general information fields
    embed.add_field(name="Owner", value=f"{guild.owner.mention} ({guild.owner.name})", inline=True)
    embed.add_field(name="Created On", value=created_at, inline=True)
    
    # Add member statistics fields
    embed.add_field(name="Total Members", value=f"{total_members}", inline=True)
    embed.add_field(name="Humans", value=f"{humans}", inline=True)
    embed.add_field(name="Bots", value=f"{bots}", inline=True)
    

    
    # Add channel statistics fields
    embed.add_field(name="Text Channels", value=f"{text_channels}", inline=True)
    embed.add_field(name="Voice Channels", value=f"{voice_channels}", inline=True)
    embed.add_field(name="Total Channels", value=f"{total_channels}", inline=True)
    
    # Add other statistics fields
    embed.add_field(name="Roles", value=f"{role_count}", inline=True)

    
    # Add server features
    if guild.features:
        embed.add_field(name="Features", value=", ".join(f"`{feature}`" for feature in guild.features), inline=False)
    
    # Add footer with bot name
    embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    
    # Send the embed
    await interaction.response.send_message(embed=embed)