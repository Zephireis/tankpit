import random
import asyncio
import aiohttp
import commands

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "*"
TOKEN = "Mjc3NTc1MTQwOTc0MjY0MzMz.DizE0g.rkkhFclCMNBYW6whhgd0_EKIZHY"

client = Bot (command_prefix=BOT_PREFIX)

@client.command(name='Alzanbot',
                description="Answers = a yes/no question with typical alzan responses.",
                brief="Answers from Alzan the great.",
                pass_context=True)


async def eight_ball(context):

    possible_responses = [
    'okay',
    'totally',
    'no',
    'huh',
    'idc',
    'thats lame',
    'yeah',
    'dont do that',
    'no that sucks',

    ]
    await client.say(random.choice(possible_responses) + "," + context.message.author.mention)

@client.command(aliases=[hi])
asunc def hello(ctx)
await ctx.send("dont talk to me fagget")








@client.event
async def on_ready():
    await client.change_presence(game=Game(name="With Kassondra"))
    print("logged in as" + client.user.name)
