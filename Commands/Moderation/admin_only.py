# Admin permission check decorator
import discord
from discord import app_commands
def admin_only():
    async def predicate(interaction: discord.Interaction):
        # Check if user has administrator permission
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="Permission Error 🚫",
                description="You must have **Administrator** permission to use this command!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Unauthorized attempt")
            try:
                # Send the permission error message asynchronously
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as e:
                print(f"[Response Error] {e}")
            # Return False to indicate that the check failed
            return False
        return True

    # Return the check for use with app_commands
    return app_commands.check(predicate)
