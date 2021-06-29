import os
import feedparser
import webbrowser
import discord
import json
import os.path
from os import path
from art_parse import splash
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
help_message = "help||"
command_list = ["ccp","counter","free"]
n_word = ["a","b"]
filterd = ["china","taiwan"]
mem = {}
social = {}
counter = {}
version = 1
CCP = False

async def id_clean(id):
    id = id.replace('@','')
    id = id.replace('>','')
    id = id.replace('<','')
    id = id.replace('!','')
    return id
async def counter_display(message):
    if len(counter) == 0:
        response = "failed to get counter"
    else:
        if "@" in message.content:
            id = message.content
            id = id.replace('/counter ','')
            id = id_clean(id)
            user = await client.fetch_user(int(id))
            user = user.name
            user = str(user)
            if user in counter:
                response = user + " said the N-Word " +  str(counter[user]) + " times." 
            else:
                response = user + " has not said the N-Word."
        else:
            response = ""
            for name in counter:
                response += name + " said the N-Word " +  str(counter[name]) + " times.\n"
    return response

async def feed_pars():
    games = ["Free games :video_game: :"]
    feed = feedparser.parse("https://steamcommunity.com/groups/GrabFreeGames/rss/")
    feed_entries = feed.entries
    for entry in feed.entries:
            article_title = entry.title
            games += [article_title]
    response = str(games)
    response = response.replace('[','')
    response = response.replace(']','')
    response = response.replace('\'','')
    response = response.replace(',','\n')
    return response
        
async def memory_init(mem,guild):
    global n_word
    global filterd    
    global CCP
    global social
    global counter
    if not (path.exists("cache")):
        os.mkdir('cache')
    file_name ="cache/cache"
    file_name +=str(guild.name) + str(version) +".json"
    if not (path.exists(file_name)):
        mem["filterd"] = filterd
        mem["n_word"] = n_word
        mem["CCP"] = CCP
        for member in guild.members:
            social.update({member.id : 1000})
        mem["social"] = social
        mem["counter"] = counter
        memory = open(file_name,'w')
        json.dump(mem,memory, indent=4)
    else:
        memory = open(file_name)
        mem = json.load(memory)
        n_word = mem["n_word"]
        filterd = mem["filterd"]
        CCP = mem["CCP"]
        social = mem["social"]
        counter = mem["counter"]
    memory.close()
    return mem
    
async def memory_save():
    memory = open(file_name,'w')
    mem["n_word"] = n_word
    mem["filterd"] = filterd
    mem["CCP"] = CCP
    mem["social"] = social
    mem["counter"] = counter
    json.dump(mem,memory, indent=4)
    memory.close()
    
@client.event
async def command_handler(message):
    content = message.content.split()
    command = content[0]
    command = command.replace('/','')
    response = help_message
    if command in command_list:
        print (command,"\n")
        if command == "free":
            response = await feed_pars()
        elif command == "counter":
            print(len(counter))
            response = await counter_display(message)
    await message.channel.send(response)
    
    
async def ccp_filter(message):
    pass
    
async def n_counter(message):
    pass
   
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            global mem
            mem = await memory_init(mem,guild)
            splash()
            print (guild.name,"id:",guild.id)
            print ("    ", str(guild.member_count) + " members:")
            for member in guild.members:
                print ("        ",member.name,"id:",member.id)
            break
    print(
        f'{client.user} v{version} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    
@client.event
async def on_member_join(member):
    id = str(member.id)
    if not(id in mem["social"]):
        mem["social"].update({id : 1000})
        memory_save()
    
@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith("/"):
            await command_handler(message)
        else:
            if CCP:
                await ccp_filter(message)
            await n_counter(message)
        
client.run(TOKEN)