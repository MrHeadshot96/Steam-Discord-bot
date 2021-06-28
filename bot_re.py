import os
import feedparser
import webbrowser
import discord
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def command_handler(command):
    pass
async def ccp_filter(message):
    pass
async def n_counter(message):
    pass
async def parser(message):
    content = list(message.content)
    with arg in  content:
        pass
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    print ( str(guild.member_count) + " members:")
    print (guild.name)
@client.event
async def on_member_join(member):
    pass
@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith("/"):
            parser(message)
        
client.run(TOKEN)