import os
import feedparser
import webbrowser
import discord
import json
import os.path
from os import path
from art_parse import splash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
help_message = "/free - free games \n/counter - n-word counter"
command_list = ["counter","free","refresh"]
n_word = ["nigger","nigga"]
filterd = ["china","taiwan"]
mem = {}
social = {}
counter = {}
version = 1
CCP = False

async def report_mes(message):
    if not (path.exists("log")):
        os.mkdir('log')
    file_name ="log/log"
    file_name +="."+str(message.guild.id)+"."+ str(message.guild.name) +".txt"
    mess = ""
    if message in command_list:
        mess += str(await time_n())+str(message.guild)+":"+str(message.author)+"used command"+str(command)
    else:
        mess += str(await time_n())+str(message.guild)+":"+str(message.author)+"\""+str(message.content)+"\""
    print (mess)
    log_f = open(file_name,'a')
    log_f.write(mess+"\n")
    log_f.close()
    
async def time_n():
    now = datetime.now()
    current_time = now.strftime("[%D|%H:%M:%S]")
    return current_time

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
    file_name +="."+str(guild.id)+"."+ str(version) +".json"
    if not (path.exists(file_name)):
        mem["guild"] = guild.name
        mem["guild.id"] = guild.id
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
    
async def memory_save(version,guild):
    file_name ="cache/cache"
    file_name +="."+str(guild.id)+"."+ str(version) +".json"
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
    if command in command_list:
        await report_mes (message)
        if command == "free":
            response = await feed_pars()
        elif command == "counter":
            response = await counter_display(message)
        elif command == "refresh":
            global mem
            mem = await memory_init(mem,message.guild)
            response = "refreshed"
        await message.channel.send(response)
    else:
        await report_mes (message)
        response = help_message
        await message.channel.send(response)
    
    
async def ccp_filter(message):
    pass
    
async def n_counter(message):
    for nword in n_word:
        if nword in message.content.lower():
            name = message.author.name
            if name in counter:
                val = counter[name]
                val2 = message.content.lower().count(nword)
                counter[name] = val + val2
            else:
                val2 = message.content.lower().count(nword)
                counter.update({name : val2})
            global version
            await memory_save(version,message.guild)
   
@client.event
async def on_ready():
    splash()
    global mem
    for guild in client.guilds:
        print(
            f'{client.user} v{version} is connected to the following guild:\n'
            f'{await time_n()}{guild.name}(id: {guild.id})\n'
        )
        print ("    ", str(guild.member_count) + " members:")
        mem = await memory_init(mem,guild)
        for member in guild.members:
            print ("        ",member.name,"id:",member.id)
    
@client.event
async def on_member_join(member):
    global mem
    mem = await memory_init(mem,member.guild)
    id = str(member.id)
    if not(id in mem["social"]):
        mem["social"].update({id : 1000})
        global version
        await memory_save(version,member.guild)
    
@client.event
async def on_message(message):
    global mem
    mem = await memory_init(mem,message.guild)
    if message.author.id != client.user.id:
        if message.content.startswith("/"):
            await command_handler(message)
        else:
            if CCP:
                await ccp_filter(message)
            await n_counter(message)
            await report_mes (message)
client.run(TOKEN)