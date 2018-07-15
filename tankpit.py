import random
import asyncio
import aiohttp

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "?"
TOKEN = "MjcxMzcwODc3NzAxMDYyNjY3.DiwnTQ.I7WcYZDw2oyRKeUOo-3PsAJQrVk"

client = Bot (command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Answers = a yes/no question.",
                brief="Answers from the beyond.",
                pass_context=True)


async def eight_ball(context):

    possible_responses = [
    'That is a resounding no',
    'It is not looking likely',
    'Too Hard to Tell',
    'it is quite possible',
    'Probably',

    ]
    await client.say(random.choice(possible_responses) + "," + context.message.author.mention)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="DESERT"))
    print("logged in as" + client.user.name)








client.run(TOKEN)
