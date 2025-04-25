import discord
from discord import app_commands
import aiohttp
import datetime
import urllib.parse

@app_commands.command(name="wikipedia", description="Search for information on Wikipedia")
@app_commands.describe(query="What you want to search for on Wikipedia")
async def wikipedia(interaction: discord.Interaction, query: str):
    # Let the user know we're processing their request
    await interaction.response.defer()
    
    # Format the query for the Wikipedia API
    search_term = urllib.parse.quote(query)
    
    # Wikipedia API URLs
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_term}&format=json"
    
    async with aiohttp.ClientSession() as session:
        # First search for articles matching the query
        async with session.get(search_url) as response:
            if response.status != 200:
                await interaction.followup.send("Sorry, I couldn't connect to Wikipedia. Please try again later.")
                return
            
            data = await response.json()
            search_results = data.get("query", {}).get("search", [])
            
            if not search_results:
                await interaction.followup.send(f"No Wikipedia results found for '{query}'.")
                return
            
            # Get the first result's page ID
            first_result = search_results[0]
            page_title = first_result.get("title")
            
            # Get the page content and thumbnail image
            content_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts|pageimages&exintro=1&explaintext=1&pithumbsize=512&titles={urllib.parse.quote(page_title)}&format=json"
            
            async with session.get(content_url) as content_response:
                if content_response.status != 200:
                    await interaction.followup.send("Sorry, I couldn't retrieve the article content from Wikipedia.")
                    return
                
                content_data = await content_response.json()
                pages = content_data.get("query", {}).get("pages", {})
                page_id = next(iter(pages))
                page_data = pages[page_id]
                extract = page_data.get("extract", "No extract available.")
                
                # Truncate long extracts
                if len(extract) > 1500:
                    extract = extract[:1500] + "..."
                
                # Create and send embed
                embed = discord.Embed(
                    title=page_title,
                    description=extract,
                    color=discord.Color.from_rgb(51, 102, 204),  # Wikipedia blue color
                    url=f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title)}"
                )
                
                # Set thumbnail if available
                if "thumbnail" in page_data.get("pageimage", {}):
                    embed.set_thumbnail(url=page_data["thumbnail"]["source"])
                
                # Get a relevant image if possible
                image_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=pageimages&format=json&pithumbsize=800"
                
                async with session.get(image_url) as img_response:
                    if img_response.status == 200:
                        img_data = await img_response.json()
                        img_pages = img_data.get("query", {}).get("pages", {})
                        img_page_id = next(iter(img_pages))
                        if "thumbnail" in img_pages[img_page_id]:
                            embed.set_image(url=img_pages[img_page_id]["thumbnail"]["source"])
                
                # Set author with Wikipedia logo
                embed.set_author(
                    name="Wikipedia",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png",
                    url="https://www.wikipedia.org/"
                )
                
                # Add date of last update
                current_time = datetime.datetime.utcnow()
                embed.timestamp = current_time
                
                # Add other related articles
                if len(search_results) > 1:
                    other_results = "\n".join([f"• [{result['title']}](https://en.wikipedia.org/wiki/{urllib.parse.quote(result['title'])})" for result in search_results[1:4]])
                    embed.add_field(name="📚 Related Articles", value=other_results, inline=False)
                
                # Add search metrics
                total_hits = data.get("query", {}).get("searchinfo", {}).get("totalhits", 0)
                embed.add_field(name="🔍 Search Results", value=f"Found {total_hits:,} articles", inline=True)
                
                # Add footer with user info and tip
                embed.set_footer(
                    text=f"Requested by {interaction.user.name} • Use /wikipedia for more searches",
                    icon_url=interaction.user.display_avatar.url if interaction.user.display_avatar else None
                )
                
                await interaction.followup.send(embed=embed)