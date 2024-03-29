# Import pycord to acces the discord api
import sqlite3
import datetime
import discord
from discord import option
from discord.ext import tasks
from discord.ext import commands

# Import the os module to access the environment variables
import os

# Import the dotenv module to access the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILDS = os.getenv('DEBUG_GUILDS')

# Set "bot" to the discord client
intents = discord.Intents.all()
bot = discord.Bot(debug_guilds=[DEBUG_GUILDS], intents=intents, slash_commands=True)
bot_version = "1.0"

# Set the database connection
conn = sqlite3.connect('database.db')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# When the bot is ready, print a message to the console, count the guilds and print the number of guilds


@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user} v{bot_version}")
	guild_count = 0
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("Trackbot is in " + str(guild_count) + " guilds.")
	count_messages_all.start()
	count_messages.start()
	# count_channel_distribution.start()
	# count_member_status.start()
	# count_member_messages.start()

# When the bot receives the command "/hello", it will respond with "Hello {name}!"
@bot.slash_command()
async def hello(ctx, name: str = None):
	name = name or ctx.author.name
	await ctx.respond(f"Hello {name}!")


@bot.slash_command(name="count", description="Count messages in a channel")
@option(name="channel", description="Specify the channel", required=False)
@option(name="user", description="Count only messages from specified user", required=False)
async def count(ctx, channel: discord.TextChannel = None, user: discord.User = None):
	channel = channel or ctx.channel
	embed = discord.Embed(title="", description="", color=0xff0000)
	embed.set_image(url="https://i.stack.imgur.com/hzk6C.gif")
	await ctx.respond(embed=embed)
	bots = 0
	users = 0
	usermessages = 0
	messages_per_date = {}

	if (user):
		async for message in channel.history(limit=None):
			if message.author.id == user.id:
				usermessages += 1
		embed = discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(
			name="Messages", value=f"In total, {user.name} has send **{usermessages}** messages in {channel}.", inline=True)
		await ctx.edit(embed=embed)

	else:
		async for message in channel.history(limit=None):
			message_date = message.created_at.date()
			if message_date not in messages_per_date:  # Add the date to the dictionary if necessary
				messages_per_date[message_date] = 0
			# Increment the number of messages on that date
			messages_per_date[message_date] += 1
			if message.author.bot == True:
				bots += 1
			else:
				users += 1
		# print(messages_per_date)
		embed = discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(
			name="Messages", value=f"In total, there are **{users+bots}** messages in **{channel}**.", inline=True)
		embed.add_field(
			name="Users", value=f"There are **{users}** messages from users in **{channel}**.", inline=True)
		embed.add_field(
			name="Bots", value=f"There are **{bots}** messages from bots in **{channel}**.", inline=True)
		await ctx.edit(embed=embed)


@bot.slash_command(name="countall", description="Count messages in all channels")
@option(name="user", description="Count only messages from specified user", required=False)
async def countall(ctx, user: discord.User = None):
	await ctx.respond("Counting messages...")
	bots = 0
	users = 0
	usermessages = 0
	messages_per_date = {}

	if (user):
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
				async for message in channel.history(limit=None):
					if message.author.id == user.id:
						usermessages += 1
		embed = discord.Embed(title="Results", description="", color=0xff0000)
		embed.add_field(
			name="Messages", value=f"In total, {user.name} has send **{usermessages}** messages in this server.", inline=True)
		await ctx.edit(embed=embed)

	else:
		for channel in ctx.guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
				async for message in channel.history(limit=None):
					message_date = message.created_at.date()
					if message_date not in messages_per_date:  # Add the date to the dictionary if necessary
						messages_per_date[message_date] = 0
					# Increment the number of messages on that date
					messages_per_date[message_date] += 1
					if message.author.bot == True:
						bots += 1
					else:
						users += 1
					print(bots+users)
		# print(messages_per_date)
		await ctx.respond(f"There are **{users+bots}** messages in this guild. **{users}** of them are from users and **{bots}** of them are from bots.")


@tasks.loop(minutes=5)
async def count_messages():
	await bot.wait_until_ready()
	print("Counting messages...")
	bots = 0
	users = 0
	guild = bot.get_guild(1021691188287373322)
	for channel in guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
			messages_per_date = {}
			async for message in channel.history(limit=None):
				message_date = message.created_at.date()
				if message_date not in messages_per_date:
					messages_per_date[message_date] = 0
				messages_per_date[message_date] += 1
				if message.author.bot == True:
					bots += 1
				else:
					users += 1
			
			cursor.execute(f'DROP TABLE IF EXISTS "{channel.name}"')
			sql = f'''CREATE TABLE "{channel.name}"(
				Date DATETIME NOT NULL,
				Count INT
				)'''
			cursor.execute(sql)
			for date in messages_per_date:
				cursor.execute(f'INSERT INTO "{channel.name}" (DATE, COUNT) VALUES (?, ?)', (date, messages_per_date[date]))
				# print(f"Added {messages_per_date[date]} messages from {date} to {channel.name}")
			# print(f"Added {channel.name} to database")

	conn.commit()
	print("Updated messages in database")
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"There are **{users+bots}** messages in this guild. **{users}** of them are from users and **{bots}** of them are from bots.")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{users+bots} messages in this guild"))


@tasks.loop(minutes=5)
async def count_channel_distribution():
	await bot.wait_until_ready()
	print("Counting channel distribution...")
	guild = bot.get_guild(1021691188287373322)
	channels = {}
	for channel in guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
			channels[channel.name] = 0
			async for message in channel.history(limit=None):
				channels[channel.name] += 1
			
	cursor.execute(f'DROP TABLE IF EXISTS ChannelDistribution')
	sql = f'''CREATE TABLE ChannelDistribution(
				Channel VARCHAR(255) NOT NULL,
				Count INT
				)'''
	cursor.execute(sql)
	for entry in channels:
		cursor.execute(f'INSERT INTO ChannelDistribution (Channel, COUNT) VALUES (?, ?)', (entry, channels[entry]))
		# print(f"Added {entry} to database")

	conn.commit()

	print("Updated channel distribution")
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"Channel distribution: {channels}")


# task to count all the messages in the whole server and put it in the database in a table called Messages
@tasks.loop(minutes=5)
async def count_messages_all():
	await bot.wait_until_ready()
	print("Counting messages...")
	guild = bot.get_guild(1021691188287373322)
	bots = 0
	users = 0
	messages_per_date = {}
	for channel in guild.channels:
			if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
				async for message in channel.history(limit=None):
					message_date = message.created_at.date()
					if message_date not in messages_per_date:  # Add the date to the dictionary if necessary
						messages_per_date[message_date] = 0
					# Increment the number of messages on that date
					messages_per_date[message_date] += 1
					if message.author.bot == True:
						bots += 1
					else:
						users += 1
					# print(bots+users)
	
	cursor.execute(f'DROP TABLE IF EXISTS Messages')
	sql = f'''CREATE TABLE Messages(
				Date VARCHAR(255) NOT NULL,
				Count INT
				)'''
	cursor.execute(sql)
	for entry in messages_per_date:
		cursor.execute(f'INSERT INTO Messages (Date, COUNT) VALUES (?, ?)', (entry, messages_per_date[entry]))
		# print(f"Added {entry} to database")

	conn.commit()
	print("Updated Messages in database")

# task to count the online, offline, idle, dnd members and put it in the database in a table called MemberStatus
@tasks.loop(minutes=5)
async def count_member_status():
	await bot.wait_until_ready()
	print("Counting member status...")
	guild = bot.get_guild(1021691188287373322)
	memberstatus = {"online": 0, "offline": 0, "idle": 0, "dnd": 0}
	for member in guild.members:
		if member.status == discord.Status.online:
			memberstatus["online"] += 1
		elif member.status == discord.Status.offline:
			memberstatus["offline"] += 1
		elif member.status == discord.Status.idle:
			memberstatus["idle"] += 1
		elif member.status == discord.Status.dnd:
			memberstatus["dnd"] += 1

	cursor.execute(f'DROP TABLE IF EXISTS MemberStatus')
	sql = f'''CREATE TABLE MemberStatus(
				Status VARCHAR(255) NOT NULL,
				Count INT
				)'''
	cursor.execute(sql)
	for entry in memberstatus:
		cursor.execute(f'INSERT INTO MemberStatus (Status, COUNT) VALUES (?, ?)', (entry, memberstatus[entry]))
		# print(f"Added {entry} to database")

	conn.commit()

	print("Updated member status")
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"Member status: {memberstatus}")

# task to count all the messages and sort them per user and put the number of messages sent by each user in the database in a table called MemberMessages
@tasks.loop(minutes=5)
async def count_member_messages():
	# await bot.wait_until_ready()
	print("Counting member messages...")
	guild = bot.get_guild(1021691188287373322)
	membermessages = {}
	for channel in guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.guild.me.guild_permissions.view_channel == True:
			async for message in channel.history(limit=None):
				message_user = message.author.name
				if message_user not in membermessages:  # Add the user to the dictionary if necessary
					membermessages[message_user] = 0
				# Increment the number of messages on that user
				membermessages[message_user] += 1

	cursor.execute(f'DROP TABLE IF EXISTS MemberMessages')
	sql = f'''CREATE TABLE MemberMessages(
				Member VARCHAR(255) NOT NULL,
				Count INT
				)'''
	cursor.execute(sql)
	for entry in membermessages:
		cursor.execute(f'INSERT INTO MemberMessages (Member, COUNT) VALUES (?, ?)', (entry, membermessages[entry]))
		# print(f"Added {entry} to database")

	conn.commit()
	print("Updated member messages")

# command to ban people (only if admin) with @option and put the username in the database in a table called Bans, create this table if it doesn't exist, but do not delete it if it does
@bot.command(name="ban", help="Bans a user from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason=None):
	await member.ban(reason=reason)
	# cursor.execute(f'DROP TABLE IF EXISTS Bans')
	# sql = f'''CREATE TABLE Bans(
	# 			Username VARCHAR(255) NOT NULL,
	# 			Reason VARCHAR(255)
	# 			)'''
	# cursor.execute(sql)
	cursor.execute(f'INSERT INTO Bans (Username, Reason) VALUES (?, ?)', (member.name, reason))
	conn.commit()
	print("Updated bans")
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"Banned {member.name} for {reason}")
	await ctx.respond(f"Banned {member.name} for {reason}")

# ping slash command to check if the bot is online and send latency
@bot.slash_command(name="ping", description="Check if the bot is online")
async def ping(ctx):
	await ctx.respond(f"Pong! {round(bot.latency*1000)}ms")

# command to unban people (only if admin) with @option and delete the username from the database in a table called Bans
@bot.command(name="unban", help="Unbans a user from the server")
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: discord.Member, reason=None):
	await member.unban(reason=reason)
	cursor.execute(f'DELETE FROM Bans WHERE Username = ?', (member.name,))
	conn.commit()
	print("Updated bans")
	channel = bot.get_channel(1081203360956420207)
	await channel.send(f"Unbanned {member.name} for {reason}")
	await ctx.respond(f"Unbanned {member.name} for {reason}")



# Run the bot with the token
bot.run(TOKEN)