import os
import feedparser
import webbrowser
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
filterd = ["china","taiwan"]
nword_list = ["nigga","nigger"]
counter_score = {"name":"value"}
client = discord.Client()
CCP = False
@client.event
async def command_handler(message):
    if "/ccp" in message.content:
        global CCP
        trig = CCP
        if trig == True:
            CCP = False
        elif trig == False:
            CCP = True
        response = "CCP filter : " + str(CCP)
        await message.channel.send(response)
    elif "/help" in message.content:
        await message.channel.send("/help - Displays this massage \n /ccp - The CCP filter \n /add_ccp - add word to CCP filter \n /free - Show free games \n /settings - Display the current settings \n /counter - N-Word counter \n /echo - echoes text back")
    elif "/add_ccp" in message.content:
        global filterd
        text = message.content
        text = text.replace('/add_ccp ','')
        if text in filterd:
            response = text + " already in list."
            await message.channel.send(response)
        else:
            filterd += [text]
            response = text + " added."
            await message.channel.send(response)
        print (filterd)
    elif "/free" in message.content:
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
        await message.channel.send(response)
    elif "/settings" in message.content:
        response = "CCP filter: " + str(CCP) + "\n" + "filter list: " + str(filterd)
        await message.channel.send(response)
    elif "/counter" in message.content:
        global counter_score
        cs = counter_score
        if "@" in message.content:
            id = message.content
            id = id.replace('/counter','')
            id = id.replace('@','')
            id = id.replace('>','')
            id = id.replace('<','')
            id = id.replace('!','')
            id = id.replace(' ','')
            user = await client.fetch_user(int(id))
            user = user.name
            user = str(user)
            if user in cs:
                response = str(cs[user]) + " times." 
            else:
                response = user + " has not said the N-Word."
        else:
            response = str(counter_score)
        response = response.replace('{','')
        response = response.replace('}','')
        response = response.replace(',','\n')
        response = response.replace('\'','')
        await message.channel.send(response)
    elif "/echo" in message.content:
        response = message.content
        response = response.replace('/echo ','')
        await message.channel.send(response)
    else:
        await message.channel.send("/help - Displays this massage \n /ccp - The CCP filter \n /add_ccp - add word to CCP filter \n /free - Show free games \n /settings - Display the current settings \n /counter - N-Word counter \n /echo - echoes text back")
@client.event
async def ccp_filter(message):
    for filter in filterd:
            if filter in message.content.lower():
                await message.delete()
                print ("deleted:[",message.content,"] -" , message.author.name, "[",message.id,"]")
                response =  message.author.name + " your message has been logged and reported." 
                await message.channel.send(response)
@client.event               
async def n_counter(message):
    for nword in nword_list:
        if nword in message.content.lower():
            name = message.author.name
            global counter_score
            cs = counter_score
            if name in cs:
                val = cs[name]
                val2 = message.content.lower().count(nword)
                cs[name] = val + val2
            else:
                val2 = message.content.lower().count(nword)
                cs.update({name : val2})
@client.event
async def on_ready():
    
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f'CCP filter:{CCP}'
    )
    
@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        if message.content.startswith("/"):
            await command_handler(message)
        elif CCP == True:
            await n_counter(message)
            await ccp_filter(message)
        else:
            await n_counter(message)
client.run(TOKEN)
