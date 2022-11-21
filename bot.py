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

# When the bot is ready, print a message to the console, count the guilds and print the number of guilds
@bot.event
async def on_ready():
	print('We have logged in as {0.user} v{1}'.format(bot, bot_version))
	guild_count = 0
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("Trackbot is in " + str(guild_count) + " guilds.")

@bot.slash_command()
async def hello(ctx, name: str = None):
	name = name or ctx.author.name
	await ctx.respond(f"Hello {name}!")

@bot.slash_command(name="count", description="Count messages in a channel")
async def count(ctx, channel: discord.TextChannel=None):
	channel = channel or ctx.channel
	await ctx.respond("Counting messages...")
	bots = 0
	users = 0
	messages_per_date = {}
	async for message in channel.history(limit=None):
		message_date = message.created_at.date()
		if message_date not in messages_per_date: # Add the date to the dictionary if necessary
			messages_per_date[message_date] = 0
		messages_per_date[message_date] += 1 # Increment the number of messages on that date
		if message.author.bot == True:
			bots += 1
		else:
			users += 1
	embed = discord.Embed(title=":calendar: Messages per day", description="Show how many messages were send each day", color=0x00FF00)
	for date in messages_per_date:
		embed.add_field(name=f"{date}", value=f"{messages_per_date[date]} messages", inline=False)
	await ctx.respond(embed=embed)
	await ctx.respond(f"There are **{users+bots}** messages in {channel}. **{users}** of them are from users and **{bots}** of them are from bots.")

@bot.slash_command(name="countall", description="Count messages in all channels")
async def countall(ctx):
	await ctx.respond("Counting messages...")
	dates = []
	bots = 0
	users = 0
	for channel in ctx.guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel== True:
			async for message in channel.history(limit=None):
				if message.author.bot == True:
					bots += 1
					dates.append(message.created_at)
				else:
					users += 1
					dates.append(message.created_at)
				print(bots+users)
	await ctx.respond(f"There are **{users+bots}** messages in this guild. **{users}** of them are from users and **{bots}** of them are from bots.")

# Run the bot with the token
bot.run(TOKEN)