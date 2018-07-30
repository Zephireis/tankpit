import random
import discord
import asyncio
import aiohttp
import requests
import json
import html5lib
import os

from discord import Game
from bs4 import BeautifulSoup
from discord.ext.commands import Bot




BOT_PREFIX = "."


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
client.run(os.getenv('TOKEN'))


#-------FUN COMMANDS--------------
@client.command(name='8ball')
async def eight_ball():
    possible_responses = [
    'that is a resounding no',
    'It is not looking likely',
    'Too hard to tell',
    'definitely',
    'idc',
    'probably',
    'sure',
    'no',
    'maybe',
    'its quite possible'

    ]
    await client.say(random.choice(possible_responses))

#------Tankpit Funny Commands-----





#-----------help command--------------
@client.command(pass_context=True)
async def help(ctx):
       embed = discord.Embed(title="How to get your tank added?", description=" DM GeneralSick#8995 to add your tank", color=0x4ec115)
       embed.add_field(name=".tanknamehere", value="Example: 'Tank_Name' not 'Tank Name'", inline=False)
       embed.add_field(name=".tpstat", value="Displays how many people are playing or waiting", inline=False)
       embed.add_field(name=".top25", value="Shows live list of current season leaderboard", inline =False)
       embed.add_field(name=".info @username", value="Information about discord user", inline=False)
       embed.add_field(name=".serverinfo", value="Server information", inline=False)
       embed.add_field(name=".help", value="displayes the help embed", inline=False)
       embed.add_field(name=".8ball", value="Answers from beyond...",inline=False)
       embed.add_field(name="Soon to come", value=".Calendar .Top25Global .addyourowntank .nexttourny", inline=False)
       embed.set_author(name="TankPit Bot help Use '.' to initiate command", icon_url='https://tankpit.com/images/icons/red_orb.png')
       embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
       embed.set_footer(text='https://tankpit.com')
       embed.set_image(url='https://tankpit.com/images/hero.png',)
       await client.send_message(ctx.message.author, embed=embed)






#-----------Server commands-------------
@client.command(pass_context=True)
async def serverinfo(ctx):
       embed = discord.Embed(title="Tankpit bot", description="Grabs api stats on player profiles", color=0x00ff00)
       embed.add_field(name="Author", value="Zephireis#8995")
       embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
       embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
       embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
       embed.add_field(name="Members", value=len(ctx.message.server.members))
       embed.add_field(name="Server count", value=f"{len(client.servers)}")
       embed.add_field(name="Invite", value="[]()")
       embed.set_thumbnail(url=ctx.message.server.icon_url)
       await client.say(embed=embed)

#--------PlayerStats commands------------
@client.command(pass_context=True)
async def GeneralSick():
        embed = discord.Embed(title="SERVICE RECORD: GeneralSick", description="",  color =0xdd3d20)
        url ='https://tankpit.com/api/tank?tank_id=3582'
        response = requests.get(url).json()

        profile = response['profile']
        other_tanks = response['other_tanks'][0]
        deac = response["map_data"]["World"]["deactivated"]
        time = response["map_data"]["World"]["time_played"]
        kills = response["map_data"]["World"]["destroyed_enemies"]
        ranks = response["map_data"]["World"]["rank"]
        lastplayed =  response["last_played"]
        location = response["country"]
        favm = response["favorite_map"]
        pong = response["ping"]
        Bio = response["profile"]
        rewards = response["awards"]

        embed.add_field(name="Deactivated", value=deac, inline=True)
        embed.add_field(name='Kills',value=kills,inline=True)
        embed.add_field(name='Last Played',value=lastplayed,inline=True)
        embed.add_field(name='Favorite map',value=favm,inline=True)
        embed.add_field(name='Bio',value=profile,inline=True)
        embed.add_field(name='Time Played',value=favm,inline=True)
        embed.add_field(name='Rank',value=ranks,inline=True)
        embed.add_field(name='Country',value=location,inline=True)
        embed.add_field(name="Ping",value=pong,inline=True)
        embed.add_field(name="Awards",value=rewards,inline=True)
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)

#----------tankpit site stats commands---------
@client.command(pass_context=True)
async def tpstat():
    embed = discord.Embed(title="", description="",  color =0xff0000)
    page= requests.get("https://tankpit.com")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(id="hero-activity")
    activity = data("p")[0].get_text()
    activity2 = data("p")[1].get_text()
    maps = data("p")[3].get_text()

    embed.add_field(name="In Game", value=activity, inline=True)
    embed.add_field(name="PreLobby", value=activity2, inline=True)
    embed.add_field(name="Map", value=maps , inline=True)
    await client.say(embed=embed)



@client.command(pass_context=True)
async def top25():
    embed = discord.Embed(title="Top25 Current season (Live updates)", description="",  color =0x00e100)
    page= requests.get("https://tankpit.com/top25")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(id="top25-page")
    one = data("td")[1].get_text()
    two = data("td")[6].get_text()
    three = data("td")[11].get_text()
    four = data("td")[16].get_text()
    five = data("td")[21].get_text()
    six = data("td")[26].get_text()
    seven = data("td")[31].get_text()
    eight = data("td")[36].get_text()
    nine = data("td")[41].get_text()
    ten = data("td")[46].get_text()
    eleven =data("td")[51].get_text()
    twelve =data("td")[56].get_text()
    thirteen =data("td")[61].get_text()
    fourteen =data("td")[66].get_text()
    fivthteen =data("td")[71].get_text()
    sixteen =data("td")[76].get_text()
    seventeen =data("td")[81].get_text()
    eightteen =data("td")[86].get_text()
    nineteen =data("td")[91].get_text()
    twenty =data("td")[96].get_text()
    twentyone =data("td")[101].get_text()
    twentytwo =data("td")[106].get_text()
    twentythree=data("td")[111].get_text()
    twentyfour=data("td")[116].get_text()
    twentyfive=data("td")[121].get_text()


    embed.add_field(name="1st", value=one, inline=True)
    embed.add_field(name="2nd", value=two, inline=True)
    embed.add_field(name="3rd", value= three, inline=True)
    embed.add_field(name="#4th", value= four, inline=True)
    embed.add_field(name="#5th", value=five , inline =True)
    embed.add_field(name="#6th", value=six , inline =True)
    embed.add_field(name="#7th", value=seven , inline =True)
    embed.add_field(name="#8th", value=eight , inline =True)
    embed.add_field(name="#9th", value=nine , inline =True)
    embed.add_field(name="#10th", value=ten , inline =True)
    embed.add_field(name="#11th", value=eleven , inline =True)
    embed.add_field(name="#12h", value=twelve , inline =True)
    embed.add_field(name="#13th", value=thirteen, inline =True)
    embed.add_field(name="#14th", value=fourteen , inline =True)
    embed.add_field(name="#15th", value=fivthteen , inline =True)
    embed.add_field(name="#16th", value=sixteen , inline =True)
    embed.add_field(name="#17th", value=seventeen , inline =True)
    embed.add_field(name="#18th", value=eightteen , inline =True)
    embed.add_field(name="#19th", value=nineteen , inline =True)
    embed.add_field(name="#20th", value=twenty , inline =True)
    embed.add_field(name="#21st", value=twentyone , inline =True)
    embed.add_field(name="#22nd", value=twentytwo, inline =True)
    embed.add_field(name="#23rd", value=twentythree , inline =True)
    embed.add_field(name="#24th", value=twentyfour , inline =True)
    embed.add_field(name="#25th", value=twentyfive , inline =True)
    await client.say(embed=embed)


#-----------events-------------------



@client.event#events = (function here) then function on the bottom to send out)
async def on_member_join(member):
    embed=discord.Embed(title="Welcome to the TankPit HQ Discord", description=" ",  color =0x7d2789)
    embed.set_thumbnail(url="https://tankpit.com/images/icons/orange_orb.png")
    embed.add_field(name="About", value="This community is a collaboration of friends, gamers and the unknown. BEWARE of the unknown At the bottom left is a cogwheel where you can access User Settings. Please set up your voice settings, profile, notifications, etc. there! If you need help,just ask! ADMIN  Only the ADMIN will have access to priority settings for the server. Please reach out to @GeneralSick  ⚒  or @Grimlock#6475 Little word of advice if you're new to the game should keep your main tank under some privacy in here or the hyenas of the community will be out to hunt you down", inline=True)
    embed.add_field(name="Rules", value="Be respectful to others \n•Please do not spam \n•Don't abuse mentions \n•Keep the drama to an A-B conversation \n•Respect the choice of music \n•If players abuse the ;;skip command, a voting policy will be in place", inline=True)
    embed.add_field(name="TankPit Bot Commands", value=".help .8ball .tankhere .serverinfo .info@username .tpstat .top25", inline=True)
    await client.send_message(member, embed=embed)
    channel = discord.utils.get(member.server.channels, name="general")
    embed=discord.Embed(title="Help! an enemy has joined the chat", description=" ",  color =0x389b2b)
    await client.send_message(channel, embed=embed)




#-----Bot Status-----------------------
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Use .help for commands"))
    print("logged in as" + client.user.name)




client.run(TOKEN)
