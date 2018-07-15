import random
import asyncio
import aiohttp

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "*"
TOKEN = "Mjc3NTc1MTQwOTc0MjY0MzMz.DizE0g.rkkhFclCMNBYW6whhgd0_EKIZHY"

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

    ]
    await client.say(random.choice(possible_responses) + "," + context.message.author.mention)


@client.event
async def on_message():
  if message.content == "hi":
   if message.author.id == ('107678929925484544'):
    choicesa = ('get away', 'dont greet me','dont talk to me fagget')
    await bibi.say(random.choice(choicesa))
  elif message.author.id == ('80971950054187008'):
    choicesl = ('lauren...', 'hi. lauren.')
    await bibi.say(random.choice(choicesl))







@client.event
async def on_ready():
    await client.change_presence(game=Game(name="With Kassondra"))
    print("logged in as" + client.user.name)
