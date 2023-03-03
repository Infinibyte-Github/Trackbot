# Import pycord to acces the discord api
import discord
from discord import option

# Import the os module to access the environment variables
import os

# Import the dotenv module to access the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS')

# Set "bot" to the discord client
bot = discord.Bot(debug_guilds=[DEBUG_GUILDS])
bot_version = "1.0"

# When the bot is ready, print a message to the console, count the guilds and print the number of guilds
@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user} v{bot_version}")
	guild_count = 0
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("Trackbot is in " + str(guild_count) + " guilds.")

# When the bot receives the command "/hello", it will respond with "Hello {name}!"
@bot.slash_command()
async def hello(ctx, name: str = None):
	name = name or ctx.author.name
	await ctx.respond(f"Hello {name}!")

# Run the bot with the token
bot.run(TOKEN)