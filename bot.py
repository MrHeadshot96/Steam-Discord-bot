import os
import feedparser
import webbrowser
import discord
import ffmpeg
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import json
import os.path
import pafy
from os import path
from art_parse import splash
from dotenv import load_dotenv
from datetime import datetime
from youtubesearchpython import VideosSearch
from discord.ext import commands

load_dotenv()
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
prefix = "/"
help_command = commands.DefaultHelpCommand( no_category = 'Commands')
client = commands.Bot(command_prefix=prefix, intents =intents, help_command = help_command)
n_word = ["nigg"]
filterd = ["china","taiwan"]
URL_1 = "https://steamcommunity.com/groups/GrabFreeGames/rss/"
mem = {}
social = {}
counter = {}
version = 1
CCP = False


class Operator_commands(commands.Cog):
    @commands.command(name='logs',brief='Show logs. *', description='Show logs from the bot. Use /logs all for logs from all servers. (operator role only)',pass_context=True)
    @commands.has_role("operator")
    async def logs_c(self, ctx, arg=''):
        message=ctx.message
        file_name = "log"
        response = "send:\n"
        if arg == "all":
            for guild in client.guilds:
                file_name +="."+str(guild.id)+"."+ str(guild.name) +".txt"
                await ctx.channel.send(file = discord.File('./log/' + file_name) )
                response += file_name + "\n"
                file_name ="log"
        else:
            file_name +="."+str(message.guild.id)+"."+ str(message.guild.name) +".txt"
            await ctx.channel.send(file = discord.File('./log/' + file_name) )
            response += file_name
        await ctx.send(response)
        
    @commands.command(name='prefix',brief='Set prefix. *', description='Changes the prefix of the bot commands. (operator role only)')
    @commands.has_role("operator")
    async def prefix_c(self, ctx, arg):
        response=""
        global prefix
        message=ctx.message
        prefix = arg
        client.command_prefix = prefix
        await memory_save(version,message.guild)
        response += "Prefix changed to " + prefix 
        await ctx.send(response)

#music player
class Music_Commands(commands.Cog):
    @commands.command(name="play",brief='Play music from youtube',description='Play music from youtube.')  
    async def play_m(self, ctx, *args):
        arg = (' '.join(args))
        print (arg)
        message = ctx.message
        response = ""
        if arg.startswith("http"):
            URL = arg
        else:
            result = VideosSearch(arg,limit = 1)
            pest = result.result()['result'][0]
            URL = pest["link"]
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
                response += "playing:\n" + URL
            else:
                if (voice.channel != message.author.voice.channel):
                    channel = message.author.voice.channel
                    await voice.move_to(message.author.voice.channel)
                if voice.is_playing():
                    voice.stop()
                    song = pafy.new(URL)  # creates a new pafy object
                    audio = song.getbestaudio()  # gets an audio source
                    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                    voice.play(source)  # play the source
                    response += "playing:\n" + URL
                else:
                    song = pafy.new(URL)  # creates a new pafy object
                    audio = song.getbestaudio()  # gets an audio source
                    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                    voice.play(source)  # play the source
        else:
            response = "You are not in a voice channel"
        await ctx.send(response)
    
    @commands.command(name="stop",brief='Stop music from youtube.',description='Stop music from youtube.')  
    async def stop_m(self, ctx):
        response = ""
        message = ctx.message
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
        await ctx.send(response)
    
    @commands.command(name="pause",brief='Pause music from youtube.',description='Pause music from youtube.')  
    async def pause_m(self, ctx):
        message = ctx.message
        response = ""
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        voice.pause()
        response += "song paused by " + message.author.name
        await ctx.send(response)
    
    @commands.command(name="resume",brief='Resume music from youtube.',description='Resume music from youtube.')  
    async def resume_m(self, ctx):
        message = ctx.message
        response = ""
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        voice.resume()
        response += "song resumed by " + message.author.name
        await ctx.send(response)

class General_Commands(commands.Cog):
    @commands.command(name="counter",brief='N word counter.',description='Show how many time a user has said the N word.')  
    async def counter_c(self, ctx):
        response = await counter_display(ctx.message)
        await ctx.send(response)
        
    @commands.command(name="free",brief='Show free games.',description='Show free games.')  
    async def free_c(self, ctx):
        response = await feed_pars(URL_1)
        await ctx.send(response)

#log message to log file . <message>
async def report_mes(message):
    ctx = await client.get_context(message)
    if not (path.exists("log")):
        os.mkdir('log')
    file_name ="log/log"
    file_name +="."+str(message.guild.id)+"."+ str(message.guild.name) +".txt"
    mess = ""
    if (ctx.valid) and (ctx.command):
        mess += str(await time_n())+str(message.guild)+":"+str(message.author)+" used command "+str(message.content)
    else:
        mess += str(await time_n())+str(message.guild)+":"+str(message.author)+" \""+str(message.content)+"\""
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
            id = await id_clean(id)
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
        client.command_prefix = prefix
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
    
async def ccp_filter(message):
    pass
    
async def n_counter(message):
    for nword in n_word:
        mess = message.content.lower()
        ''.join(e for e in mess if e.isalnum())
        val2 = mess.count(nword)
        name = message.author.name
        if name in counter:
            val = counter[name]
            counter[name] = val + val2
        else:
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
        await report_mes (message)
        if CCP:
            await ccp_filter(message)
        await n_counter(message)
    await client.process_commands(message)

client.add_cog(Operator_commands())
client.add_cog(Music_Commands())
client.add_cog(General_Commands())
client.run(TOKEN)