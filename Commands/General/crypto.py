import aiohttp
import discord
from discord import app_commands
import datetime
# Function to fetch supported coins from CoinGecko API
async def fetch_coins():
    global coin_list
    url = "https://api.coingecko.com/api/v3/coins/list"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    coin_list = [{"name": f"{coin['name']} ({coin['symbol'].upper()})", "id": coin["id"]} for coin in data]
                else:
                    print(f"Error occurred while fetching the coin list. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while fetching the coins: {e}")

# Crypto currency command
@app_commands.command(name="crypto", description="Displays cryptocurrency data.")
@app_commands.describe(coin="The cryptocurrency you want to see the data for.")
async def crypto_command(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()

    url = f"https://api.coingecko.com/api/v3/coins/{coin}"

    async with aiohttp.ClientSession() as session:
        try:
            # Fetch cryptocurrency data from CoinGecko API
            async with session.get(url, params={"localization": "false", "market_data": "true"}) as response:
                if response.status != 200:
                    await interaction.followup.send(f"An error occurred while fetching cryptocurrency data. Status code: {response.status}")
                    return

                data = await response.json()
                market_data = data.get("market_data", {})

                name = data.get("name", "")
                symbol = data.get("symbol", "").upper()
                image = data.get("image", {}).get("large", "")
                current_price = market_data.get("current_price", {}).get("usd", "Unknown")
                price_change_24h_percentage = market_data.get("price_change_percentage_24h", 0)
                market_cap = market_data.get("market_cap", {}).get("usd", "Unknown")
                total_volume = market_data.get("total_volume", {}).get("usd", "Unknown")

                # Set color based on price change (green for positive, red for negative)
                color = discord.Color.green() if price_change_24h_percentage > 0 else discord.Color.red()
                arrow = "↗️" if price_change_24h_percentage > 0 else "↘️"

                # Create an embed to display the crypto data
                embed = discord.Embed(
                    title=f"{name} ({symbol}) Data",
                    description=f"Current data for the cryptocurrency **{name}**",
                    color=color,
                    url=f"https://www.coingecko.com/en/coins/{coin}",
                    timestamp=datetime.datetime.now(datetime.UTC)
                )

                # Add fields to the embed
                embed.add_field(name="Current Price", value=f"$ {current_price:,.2f}", inline=True)
                embed.add_field(name="24h Price Change", value=f"{arrow} %{abs(price_change_24h_percentage):.2f}", inline=True)
                embed.add_field(name="Market Cap", value=f"$ {market_cap:,.0f}", inline=True)
                embed.add_field(name="24h Trading Volume", value=f"$ {total_volume:,.0f}", inline=True)

                # Set thumbnail image if available
                if image:
                    embed.set_thumbnail(url=image)

                embed.set_footer(text="Source: CoinGecko")
                await interaction.followup.send(embed=embed)

        except Exception as e:
            # Handle any errors that occur during the process
            await interaction.followup.send(f"An error occurred: {str(e)}")

# Cryptocurrency autocomplete function
@crypto_command.autocomplete("coin")
async def coin_autocomplete(interaction: discord.Interaction, current: str):
    if not current:
        return []
    # Provide suggestions based on the user's input
    suggestions = [
        app_commands.Choice(name=coin["name"], value=coin["id"])
        for coin in coin_list if current.lower() in coin["name"].lower()
    ][:25]  # Limit the suggestions to 25 items
    return suggestions
