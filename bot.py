import os
import feedparser
import webbrowser
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "deal":
        

        feed = feedparser.parse("https://steamcommunity.com/groups/GrabFreeGames/rss/")

        # feed_title = feed['feed']['title']  # NOT VALID
        feed_entries = feed.entries

        for entry in feed.entries:
                article_title = entry.title
                article_link = entry.link
                article_published_at = entry.published # Unicode string
                article_published_at_parsed = entry.published_parsed # Time object
                content = entry.summary
                response = ("{}[{}]".format(article_title, article_link))
                await message.channel.send(response)
                # print ("Published by {}".format(article_author)) 
        response = "**** END OF REPORT ****"
        await message.channel.send(response)
client.run(TOKEN)
