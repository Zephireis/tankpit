import random
import asyncio
import aiohttp

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "?"
TOKEN = "MjcxMzcwODc3NzAxMDYyNjY3.DiwnTQ.I7WcYZDw2oyRKeUOo-3PsAJQrVk"

client = Bot (command_prefix=BOT_PREFIX)

@client.command(name='Alzan',
                description="Answers = a yes/no question with typical alzan responses.",
                brief="Answers from Alzan the great.",
                pass_context=True)


async def eight_ball(context):

    possible_responses = [
    'okay',
    'sure',
    'no',
    'huh',
    'idc'
    'thats lame'
    'yeah'

    ]
    await client.say(random.choice(possible_responses) + "," + context.message.author.mention)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="With Kassondra"))
    print("logged in as" + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json() ['bpi']['USD']['rate']
    await client.say("Bitcoin price is: $" + value)





client.run(TOKEN)
