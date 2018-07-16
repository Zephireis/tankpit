import random
import asyncio
import aiohttp

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "*"
TOKEN = "Mjc3NTc1MTQwOTc0MjY0MzMz.Di2RBQ.7ykAa_A8V5Y8eVEGxsApig_F-SA"

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
    'idc',
    'thats lame',
    'yeah',
    'dont do that',
    'no that sucks',
    'totally'

    ]
    await client.say(random.choice(possible_responses) + " " + context.message.author.mention)  

    
    
    
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="With Kassondra"))
    print("logged in as" + client.user.name)
    
    
    
    
client.run(TOKEN)
