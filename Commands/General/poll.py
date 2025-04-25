import discord
from discord import app_commands
from Commands.Moderation.admin_only import admin_only
import random

# Poll Colors for the bot's polls
POLL_COLORS = [
    discord.Color.blue(),
    discord.Color.purple(),
    discord.Color.green(),
    discord.Color.gold(),
]

# Active polls storage to manage them
active_polls = {}


@app_commands.command(name="poll", description="Create a dynamic poll with selectable options. Separate options with a comma.")
@admin_only()
async def create_poll(interaction: discord.Interaction, title: str, options: str):
    # Convert options separated by commas into a list
    options = [option.strip() for option in options.split(',')]

    # Filter out empty options
    options = [option for option in options if option]

    # Ensure there are at least 2 options for the poll
    if len(options) < 2:
        await interaction.response.send_message("You must provide at least 2 options for the poll.", ephemeral=True)
        return

    # Ensure there are no more than 25 options for the poll
    if len(options) > 25:
        await interaction.response.send_message("You can add a maximum of 25 options.", ephemeral=True)
        return

    # Create buttons for the poll
    view = discord.ui.View(timeout=None)

    poll_data = {
        "title": title,
        "options": options,
        "votes": {option: [] for option in options},
        "voters": set(),
        "color": random.choice(POLL_COLORS)  # Random color from the available poll colors
    }

    # Add a button for each option
    for option in options:
        button = PollButton(option, poll_data)
        view.add_item(button)

    # Create the poll embed
    embed = create_poll_embed(title, poll_data)

    # Send the poll with the embed and buttons
    await interaction.response.send_message(embed=embed, view=view)
    response = await interaction.original_response()

    # Associate the poll data with the message ID
    active_polls[response.id] = poll_data

# Poll Buttons class
class PollButton(discord.ui.Button):
    def __init__(self, option, poll_data):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=option,
            custom_id=f"poll:{option}"
        )
        self.option = option
        self.poll_data = poll_data

    async def callback(self, interaction: discord.Interaction):
        # Check if the user has already voted
        if interaction.user.id in self.poll_data["voters"]:
            # Find and remove the previous vote
            for opt in self.poll_data["options"]:
                if interaction.user.id in self.poll_data["votes"][opt]:
                    self.poll_data["votes"][opt].remove(interaction.user.id)

        # Save the new vote
        self.poll_data["votes"][self.option].append(interaction.user.id)
        self.poll_data["voters"].add(interaction.user.id)

        # Update the poll embed with the new vote
        embed = create_poll_embed(self.poll_data["title"], self.poll_data)
        await interaction.response.edit_message(embed=embed)
# Function to create the poll embed
def create_poll_embed(title, poll_data):
    embed = discord.Embed(
        title=f"📊 {title}",
        color=poll_data["color"]
    )

    # Calculate total votes
    total_votes = sum(len(votes) for votes in poll_data["votes"].values())

    # Create the description for each option
    description = []
    for option in poll_data["options"]:
        vote_count = len(poll_data["votes"][option])
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0

        # Construct the option text
        description.append(f"**{option}**: {vote_count} votes ({percentage:.1f}%)")

    embed.description = "\n".join(description)

    # Footer with total votes
    embed.set_footer(text=f"Total votes: {total_votes}")

    return embed
