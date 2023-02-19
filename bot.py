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
DEBUG_GUILD = os.getenv('DEBUG_GUILD')

# Set "bot" to the discord client
bot = discord.Bot(debug_guilds=[DEBUG_GUILD])
bot_version = "1.0"

# Run the bot with the token
bot.run(TOKEN)