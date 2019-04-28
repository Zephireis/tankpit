import discord
from discord.ext.commands import Bot

TOKEN = "MjcxMzcwODc3NzAxMDYyNjY3.D0c35A.EQYFgFoWeKtyXs5PN5ZatKdSHSc"
BOT_PREFIX = "!"

client = Bot(command_prefix=BOT_PREFIX)

@client.command()
async def ping():
    await client.say("pong")


client.run(TOKEN)
