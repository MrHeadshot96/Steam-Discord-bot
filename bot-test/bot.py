import os
import feedparser
import webbrowser
import discord
import json
import os.path
from os import path
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
n_word = []
filterd = []
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
    
async def memory_init(mem,CCP,social,guild,counter):
    if not (path.exists("cache")):
        os.mkdir('cache')
    file_name ="cache\cache"
    file_name +=str(guild.name) + str(version) +".json"
    if not (path.exists(file_name)):
        mem["filterd"] = ["china","taiwan"]
        mem["n_word"] = ["a","b"]
        mem["CCP"] = CCP
        for member in guild.members:
            social.update({member.id : 1000})
        mem["social"] = social
        mem["counter"] = {}
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
        print (mem)
    memory.close()
    
async def memory_save():
    memory = open(file_name,'w')
    mem["n_word"] = n_word
    mem["filterd"] = filterd
    mem["CCP"] = CCP
    mem["social"] = social
    mem["counter"] = counter
    json.dump(mem,memory, indent=4)
    memory.close()
    
async def command_handler(message):
    content = message.content.split()
    command_handler(content)
    if content[0] in command_list:
        pass
    else:
        pass
    
async def ccp_filter(message):
    pass
    
async def n_counter(message):
    pass
   
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            await memory_init(mem,CCP,social,guild,counter)
            print (guild.name,"id:",guild.id)
            print ("    ", str(guild.member_count) + " members:")
            for member in guild.members:
                print ("        ",member.name,"id:",member.id)
            break
    print(
        f'{client.user} is connected to the following guild:\n'
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