# Import pycord to acces the discord api
import discord
from discord import option
from discord.ext import tasks

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
	count_messages.start()

# When the bot receives the command "/hello", it will respond with "Hello {name}!"
@bot.slash_command()
async def hello(ctx, name: str = None):
	name = name or ctx.author.name
	await ctx.respond(f"Hello {name}!")


@bot.slash_command(name="count", description="Count messages in a channel")
@option(name="channel", description="Specify the channel", required=False)
@option(name="user", description="Count only messages from specified user", required=False)
async def count(ctx, channel: discord.TextChannel=None, user: discord.User=None):
	channel = channel or ctx.channel
	embed=discord.Embed(title="", description="", color=0xff0000)
	embed.set_image(url="https://i.stack.imgur.com/hzk6C.gif")
	await ctx.respond(embed=embed)
	bots = 0
	users = 0
	usermessages = 0
	messages_per_date = {}
	
	if(user):
		async for message in channel.history(limit=None):
			if message.author.id == user.id:
				usermessages+=1
		embed=discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(name="Messages", value=f"In total, {user.name} has send **{usermessages}** messages in {channel}.", inline=True)
		await ctx.edit(embed=embed)
						
	else:
		async for message in channel.history(limit=None):
			message_date = message.created_at.date()
			if message_date not in messages_per_date: # Add the date to the dictionary if necessary
				messages_per_date[message_date] = 0
			messages_per_date[message_date] += 1 # Increment the number of messages on that date
			if message.author.bot == True:
				bots += 1
			else:
				users += 1
		# print(messages_per_date)
		embed=discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(name="Messages", value=f"In total, there are **{users+bots}** messages in **{channel}**.", inline=True)
		embed.add_field(name="Users", value=f"There are **{users}** messages from users in **{channel}**.", inline=True)
		embed.add_field(name="Bots", value=f"There are **{bots}** messages from bots in **{channel}**.", inline=True)
		await ctx.edit(embed=embed)

@bot.slash_command(name="countall", description="Count messages in all channels")
@option(name="user", description="Count only messages from specified user", required=False)
async def countall(ctx, user: discord.User=None):
	await ctx.respond("Counting messages...")
	bots = 0
	users = 0
	usermessages = 0
	messages_per_date = {}

	if(user):
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel== True:
				async for message in channel.history(limit=None):
					if message.author.id == user.id:
						usermessages+=1
		embed=discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(name="Messages", value=f"In total, {user.name} has send **{usermessages}** messages in this server.", inline=True)
		await ctx.edit(embed=embed)

	else:
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel== True:
				async for message in channel.history(limit=None):
					message_date = message.created_at.date()
					if message_date not in messages_per_date: # Add the date to the dictionary if necessary
						messages_per_date[message_date] = 0
					messages_per_date[message_date] += 1 # Increment the number of messages on that date
					if message.author.bot == True:
						bots += 1
					else:
						users += 1
					print(bots+users)
		print(messages_per_date)
		await ctx.respond(f"There are **{users+bots}** messages in this guild. **{users}** of them are from users and **{bots}** of them are from bots.")


@tasks.loop(minutes=5)
async def count_messages():
	await bot.wait_until_ready()
	print("Counting messages...")
	bots = 0
	users = 0
	messages_per_date = {}
	guild = bot.get_guild(1021691188287373322)
	for channel in guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel== True:
			async for message in channel.history(limit=None):
				message_date = message.created_at.date()
				if message_date not in messages_per_date:
					messages_per_date[message_date] = 0
				messages_per_date[message_date] += 1
				if message.author.bot == True:
					bots += 1
				else:
					users += 1
	print(bots+users)
	# print(messages_per_date)
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"There are **{users+bots}** messages in this guild. **{users}** of them are from users and **{bots}** of them are from bots.")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{users+bots} messages in this guild"))

# Run the bot with the token
bot.run(TOKEN)