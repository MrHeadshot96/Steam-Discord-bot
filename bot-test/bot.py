import os
import feedparser
import webbrowser
import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import json
import os.path
import pafy
from os import path
from art_parse import splash
from dotenv import load_dotenv
from datetime import datetime
from youtubesearchpython import VideosSearch

load_dotenv()
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
help_message = ["free        - free games\n",
                "counter - n-word counter\n",
                "play       - play music from youtube\n",
                "refresh  - refreshes memory (operator only!)\n",
                "prefix    - change bot command prefix (operator only!)\n",
                "log          - upload logs (operator only!)\n"]
command_list = ["counter","free","refresh","log","prefix","play","stop"]
n_word = ["nigg"]
filterd = ["china","taiwan"]
prefix = "/"
URL_1 = "https://steamcommunity.com/groups/GrabFreeGames/rss/"
mem = {}
social = {}
counter = {}
version = 1
CCP = False
#music player
async def play_m(message,par):
    response = ""
    URL = par
    if not(message.author.voice == None):
        channel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if (voice == None):
            channel = message.author.voice.channel
            vc = await channel.connect()
            song = pafy.new(URL)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
            vc.play(source)  # play the source
            response += "Connected to " + str(message.author.voice.channel)
        elif (voice.channel != message.author.voice.channel):
            channel = message.author.voice.channel
            await voice.move_to(message.author.voice.channel)
            response += "Connected to " + str(message.author.voice.channel)
        else:
            response += "Already connected to " + str(voice.channel)
    else:
        response = "You are not in a voice channel"
    return response
async def stop_m(message,par):
    response = ""
    if not(message.author.voice == None):
        channel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if (voice != None):
            channel = message.author.voice.channel
            await voice.disconnect()
            response += "Disconnected from " + str(voice.channel)
        else:
            response += "I am not connected "
    else:
        response = "You are not in a voice channel"
    return response
#log message to log file . <message>
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
#get current time.
async def time_n():
    now = datetime.now()
    current_time = now.strftime("[%D|%H:%M:%S]")
    return current_time
#clean trash characters of from member.id
async def id_clean(id):
    id = id.replace('@','')
    id = id.replace('>','')
    id = id.replace('<','')
    id = id.replace('!','')
    return id
#command to display n_counter values in a neat way
async def counter_display(message):
    if len(counter) == 0:
        response = "failed to get counter"
    else:
        if "@" in message.content:
            id = message.content
            id = id.replace((prefix + 'counter '),'')
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
#RSS parser (RSS URL)
async def feed_pars(URL):
    games = ""
    f = feedparser.parse(URL)
    games += f.feed.title + "\n"
    for entry in f.entries:
            article_title = entry.title
            artticle_date = entry.published_parsed
            
            games += str([article_title])+" - "+str(artticle_date[2])+"."+ str(artticle_date[1])+"."+ str(artticle_date[0])+ "\n"
    response = str(games)
    response = response.replace('[','')
    response = response.replace(']','')
    response = response.replace('\'','')
    response = response.replace(',','\n')
    return response
#memory initialization/refresh       
async def memory_init(mem,guild):
    global n_word
    global filterd    
    global CCP
    global social
    global counter
    global prefix
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
        mem["prefix"] = prefix
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
        prefix = mem["prefix"]
    memory.close()
    return mem
#save memory
async def memory_save(version,guild):
    file_name ="cache/cache"
    file_name +="."+str(guild.id)+"."+ str(version) +".json"
    memory = open(file_name,'w')
    mem["n_word"] = n_word
    mem["filterd"] = filterd
    mem["CCP"] = CCP
    mem["social"] = social
    mem["counter"] = counter
    mem["prefix"] = prefix
    json.dump(mem,memory, indent=4)
    memory.close()
        
async def command_handler(message):
    global prefix
    global version
    content = message.content.split()
    command = content[0]
    response = ""
    par1 = ""
    if (len(content) > 1):
        par1 = content[1]
    command = command.replace(prefix,'')
    if command in command_list:
        await report_mes (message)
        if command == "free":
            response = await feed_pars(URL_1)
        elif command == "counter":
            response = await counter_display(message)
        elif command == "play":
            response = await play_m(message,par1)
        elif command == "stop":
            response = await stop_m(message,par1)
        elif command == "refresh":
            if ("operator" in [y.name.lower() for y in message.author.roles]):
                global mem
                mem = await memory_init(mem,message.guild)
                response = "refreshed"
            else:
                response += message.author.name + " not operator"
        elif (command == "log"):
            if ("operator" in [y.name.lower() for y in message.author.roles]):
                file_name = "log"
                if par1 == "all":
                    response = "send:\n"
                    for guild in client.guilds:
                        file_name +="."+str(guild.id)+"."+ str(guild.name) +".txt"
                        await message.channel.send(file = discord.File('./log/' + file_name) )
                        response += file_name + "\n"
                        file_name ="log"
                else:
                    file_name +="."+str(message.guild.id)+"."+ str(message.guild.name) +".txt"
                    await message.channel.send(file = discord.File('./log/' + file_name) )
                    response += file_name
            else:
                response += message.author.name + " not operator"
        elif (command == "prefix"):
            if ("operator" in [y.name.lower() for y in message.author.roles]):
                prefix = par1
                await memory_save(version,message.guild)
                response += "Prefix changed to \"" + prefix + "\""
            else:
                response += message.author.name + " not operator"
        await message.channel.send(response)
    else:
        await report_mes (message)
        for mess_line in help_message:
            response += prefix + mess_line
        await message.channel.send(response)
        
async def ccp_filter(message):
    pass
    
async def n_counter(message):
    for nword in n_word:
        mess = message.content.lower()
        ''.join(e for e in mess if e.isalnum())
        if nword in mess:
            name = message.author.name
            if name in counter:
                val = counter[name]
                for nword in mess:
                    val2 =+ 1
                counter[name] = val + val2
            else:
                for nword in mess:
                    val2 =+ 1
                counter.update({name : val2})
            global version
            await memory_save(version,message.guild)

@client.event
async def on_ready():
    splash()
    global mem
    print(
        f'{client.user} v{version} is connected to the following guild:\n'
    )
    for guild in client.guilds:
        print(
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
        if message.content.startswith(prefix):
            await command_handler(message)
        else:
            if CCP:
                await ccp_filter(message)
            await n_counter(message)
            await report_mes (message)
client.run(TOKEN)