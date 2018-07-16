import random
import asyncio
import aiohttp
import discord

from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = "!"
TOKEN = "Mjc3NTc1MTQwOTc0MjY0MzMz.Di2RBQ.7ykAa_A8V5Y8eVEGxsApig_F-SA"

client = Bot (command_prefix=BOT_PREFIX)
client.remove_command('help')

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
    
    
    
@client.command()
async def hello():
    await client.say("dont talk to me faggot")
    
    
    
@client.command(pass_context=True)
async def help(ctx):
       embed = discord.Embed(title="Use '!' to Active Alzan2.7 Commands", description="Alzan27 Commands:", color=0xeee657)
       embed.add_field(name="!Alzan", value="Alzan Answers a question 8Ball style", inline=False)
       embed.add_field(name="!hello", value="Gives a nice greet message", inline=False)
       embed.add_field(name="!serverinfo", value="gives info for the server.", inline=False)
       embed.add_field(name="!info @(namehere)", value="Gives a little info about a user", inline=False)
       embed.add_field(name="!help", value="Gives this message", inline=False)
       await client.say(embed=embed)   
    
    
    
@client.command(pass_context=True)
async def serverinfo(ctx):
       embed = discord.Embed(title="Alzan2.7", description="Dont talk to me", color=0x00ff00)
       embed.add_field(name="Author", value="Zephireis#8995")
       embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
       embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
       embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
       embed.add_field(name="Members", value=len(ctx.message.server.members))
       embed.add_field(name="Server count", value=f"{len(client.servers)}")
       embed.add_field(name="Invite", value="[https://discordapp.com/api/oauth2/authorize?client_id=277575140974264333&scope=bot&permissions=1](https://discordapp.com/api/oauth2/authorize?client_id=277575140974264333&permissions=67632193&scope=bot)")
       embed.set_thumbnail(url=ctx.message.server.icon_url)
       await client.say(embed=embed)



@client.command(pass_context=True)
async def info(ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s info".format(user.name), description="okay.", color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Joined", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        await client.say(embed=embed)
        
        
        
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="With Kassondra"))
    print("logged in as" + client.user.name)








client.run(TOKEN)
