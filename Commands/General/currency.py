import aiohttp
from dotenv import load_dotenv
import os
import discord
from discord import app_commands
import datetime
# Load environment variables from .env file
load_dotenv()
# API Keys and Basic Data
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
coin_list = []

# Supported currencies and tracked currencies
CURRENCY_OPTIONS = [
    ("US Dollar", "USD"),
    ("Euro", "EUR"),
    ("Turkish Lira", "TRY"),
    ("British Pound", "GBP"),
    ("Japanese Yen", "JPY"),
    ("Chinese Yuan", "CNY"),
    ("Canadian Dollar", "CAD"),
    ("Australian Dollar", "AUD"),
    ("Swiss Franc", "CHF")
]
TRACKED_CURRENCIES = ["USD", "EUR", "TRY", "GBP", "JPY", "CNY", "CAD", "AUD", "CHF"]



# Currency conversion command
@app_commands.command(name="currency", description="Shows the current currency exchange rates.")
@app_commands.describe(base_currency="Select the base currency unit")
@app_commands.choices(base_currency=[
    app_commands.Choice(name=name, value=code) for name, code in CURRENCY_OPTIONS
])
async def currency_command(interaction: discord.Interaction, base_currency: str = "USD"):
    await interaction.response.defer()

    # Construct URL for fetching exchange rates
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={CURRENCY_API_KEY}&base_currency={base_currency.upper()}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await interaction.followup.send(f"An error occurred while fetching exchange rates. Status code: {response.status}")
                    return

                data = await response.json()

                if "data" not in data:
                    await interaction.followup.send("No valid data received. API response: " + str(data))
                    return

                rates = data["data"]
                currency_names = {currency: name for name, currency in CURRENCY_OPTIONS}

                embed = discord.Embed(
                    title=f"Current Currency Exchange Rates",
                    description=f"Base Currency: **{currency_names.get(base_currency.upper(), base_currency.upper())}** ({base_currency.upper()})",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.now()
                )

                # Currency symbols for display
                symbols = {
                    "USD": "$", "EUR": "€", "TRY": "₺", "GBP": "£", "JPY": "¥",
                    "CNY": "¥", "CAD": "C$", "AUD": "A$", "CHF": "Fr"
                }

                displayed_currencies = 0
                for currency in TRACKED_CURRENCIES:
                    if currency == base_currency.upper():
                        conversion_text = f"1 {base_currency.upper()} = 1.0000"
                    elif currency in rates:
                        rate = rates[currency]
                        conversion_text = f"1 {base_currency.upper()} = {symbols.get(currency, '')} {rate:.4f}"
                    else:
                        continue
                    
                    embed.add_field(name=f"{currency_names.get(currency, currency)} ({currency})", value=conversion_text, inline=True)
                    displayed_currencies += 1

                # If less than 9 currencies are displayed, add empty fields for visual balance
                while displayed_currencies < 9:
                    embed.add_field(name="\u200b", value="\u200b", inline=True)
                    displayed_currencies += 1

                embed.set_footer(text="Source: FreeCurrency API • Last Updated")
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2529/2529396.png")

                await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")
