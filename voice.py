import discord
from discord.ext import commands, tasks
import jdatetime
from logging import getLogger
import sqlite3
from datetime import datetime , timedelta
import pytz
import asyncio

con = sqlite3.connect('totalmic.db')

cur = con.cursor()
# # cur.execute('''CREATE TABLE MIC
#          (ID INT PRIMARY KEY     NOT NULL,
#          COUNT           INT    NOT NULL);''')

# infos = ("INSERT INTO MIC (ID,COUNT) VALUES (? , ?)");
# data = (1 , 24)
# cur.execute(infos, data)
# con.commit()

client = commands.AutoShardedBot(command_prefix='r!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)
TOKEN = ""

@client.event
async def on_ready():
    status_task.start()
    log = getLogger("client")
    log.info(f'logged in as {client.user} , ID: {client.user.id}')
    print(f'logged in as {client.user.name}')



@client.command(pass_context = True)
async def joinchannel(ctx):
    print (ctx.author.voice.channel)
    if (ctx.author.voice.channel):
        channel = ctx.author.voice.channel
        await channel.connect()

@client.command(pass_context = True)
async def total_all(ctx):
    total_mic.start(ctx)
@client.event
async def on_voice_state_update(member, before, after):
    voice=[]
    for v in member.guild.voice_channels:
        for user in v.members:
            voice.append(user)
        count = len(voice)
        count = [int(count)]
        cur.execute("UPDATE MIC set COUNT = (?) where ID = 1" , (count))
        # cur.execute(infos, count)
        con.commit()
        # await member.guild.me.edit(nick=f'total mic: {count}')

@tasks.loop(seconds=90)
async def total_mic(ctx):

    sqlite_select_query = """SELECT * from MIC"""
    cur.execute(sqlite_select_query)
    records = cur.fetchall()
    for row in records:
        count = row[1]    
    await ctx.guild.me.edit(nick=f'total mic: {count}')


@tasks.loop()
async def status_task():
    await client.change_presence(status=discord.Status.online , activity=discord.Activity(type=discord.ActivityType.watching, name="parham-programming.ir"))
    await asyncio.sleep(3)
    await client.change_presence(status=discord.Status.idle ,activity=discord.Activity(type=discord.ActivityType.watching, name="ONLINE SHOP"))
    await asyncio.sleep(3)
    await client.change_presence(status=discord.Status.dnd ,activity=discord.Activity(type=discord.ActivityType.watching, name="ONLINE SHOP"))
    await asyncio.sleep(3)
    
client.run(TOKEN)