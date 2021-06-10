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
filterd = ["china","taiwan"]
nword_list = ["nigga","nigger"]
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
        await message.channel.send("/help - Displays this massage \n /ccp - The CCP filter \n /add_ccp - add word to CCP filter \n /free - Show free games \n /counter - N-Word counter \n /echo - echoes text back")
    elif "/add_ccp" in message.content:
        with open('filtered.json') as filtered:
            filterd = json.load(filtered)
        text = message.content
        text = text.replace('/add_ccp ','')
        if text in filterd:
            response = text + " already in list."
            await message.channel.send(response)
        else:
            filterd += [text]
            response = text + " added."
            await message.channel.send(response)
        with open('filtered.json','w') as filtered:
            json.dump(filterd,filtered)
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
    elif "/data" in message.content:
        with open('filtered.json') as filtered:
            filterd = json.load(filtered)
        with open('counter.json') as counter:
            cs = json.load(counter)
        with open('social.json') as social:
            sc = json.load(social)
        response = "CCP filter: " + str(CCP) + "\n" + "filter list: " + str(filterd) + "\n \n" + str(cs) + "\n \n" + str(sc)
        await message.channel.send(response)
    elif "/counter" in message.content:
        with open('counter.json') as counter:
            cs = json.load(counter)
        if "@" in message.content:
            id = message.content
            id = id.replace('/counter ','')
            id = id.replace('@','')
            id = id.replace('>','')
            id = id.replace('<','')
            id = id.replace('!','')
            user = await client.fetch_user(int(id))
            user = user.name
            user = str(user)
            if user in cs:
                response = user + " said the N-Word " +  str(cs[user]) + " times." 
            else:
                response = user + " has not said the N-Word."
        else:
            response = ""
            for name in cs:
                response += name + " said the N-Word " +  str(cs[name]) + " times.\n"
        await message.channel.send(response)
    elif "/credit" in message.content:
        with open('social.json') as social:
            sc = json.load(social)
        if "@" in message.content:
            id = message.content
            id = id.replace('/credit ','')
            id = id.replace('@','')
            id = id.replace('>','')
            id = id.replace('<','')
            id = id.replace('!','')
            user = await client.fetch_user(int(id))
            user = str(user.name)
            response = user + "  = " +  str(sc[id]) + " points." 
        else:
            response = ""
            for id in sc:
                user = await client.fetch_user(int(id))
                response += str(user.name) + " = " +  str(sc[id]) + " points.\n"
        await message.channel.send(response)
    elif "/echo" in message.content:
        response = message.content
        response = response.replace('/echo ','')
        await message.delete()
        await message.channel.send(response)
    else:
        await message.channel.send("/help - Displays this massage \n /ccp - The CCP filter \n /add_ccp - add word to CCP filter \n /free - Show free games \n /counter - N-Word counter \n /echo - echoes text back")
@client.event
async def ccp_filter(message):
    with open('filtered.json') as filtered:
        filterd = json.load(filtered)
    for filter in filterd:
            if filter in message.content.lower():
                await message.delete()
                print ("deleted:[",message.content,"] -" , message.author.name, "[",message.id,"]")
                with open('social.json') as social:
                    sc = json.load(social)
                U_id = str(message.author.id)
                print (U_id)
                val = sc[U_id] - 5
                sc[U_id] = val
                with open('social.json','w') as social_W:
                    json.dump(sc,social_W)
                response =  message.author.name + " your message has been logged and reported. Currently " + str(val) + " points." 
                await message.channel.send(response)
@client.event               
async def n_counter(message):
    for nword in nword_list:
        if nword in message.content.lower():
            name = message.author.name
            with open('counter.json') as counter:
                cs = json.load(counter)
            if name in cs:
                val = cs[name]
                val2 = message.content.lower().count(nword)
                cs[name] = val + val2
            else:
                val2 = message.content.lower().count(nword)
                cs.update({name : val2})
            with open('counter.json','w') as counter:
                json.dump(cs,counter)
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
    print ( str(guild.member_count) + " members:")
    print (guild.name)
    filesize = os.path.getsize("social.json")
    if filesize == 0:
        arr = {"EMPTY":0}
        arr.popitem()
        for member in guild.members:
            if member.name == client.user.name:
                pass
            else:
                print (member.id)
                arr[member.id] = 1000
                with open('social.json','w') as Soc_Cre_W:
                        json.dump(arr,Soc_Cre_W)
    else:
        with open('social.json') as Soc_Cre:
            sc_data = json.load(Soc_Cre)
        for member in guild.members:
            if member.name == client.user.name:
                pass
            else:
                print (member.id)
                if str(member.id) in sc_data:
                    pass
                else:
                    sc_data.update({member.id : 1000})
                    with open('social.json','w') as Soc_Cre_W:
                        json.dump(sc_data,Soc_Cre_W)
    with open('counter.json') as counter:
        db_data = json.load(counter)
    with open('filtered.json') as filtered:
        db_data_2 = json.load(filtered)
    print (db_data)
    print (db_data_2)

@client.event
async def on_member_join(member):
    id = str(member.id)
    with open('social.json') as Soc_Cre:
            sc_data = json.load(Soc_Cre)
    if id in sc_data:
        pass
    else:
        sc_data.update({id : 1000})
        with open('social.json','w') as Soc_Cre_W:
            json.dump(sc_data,Soc_Cre_W)
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
