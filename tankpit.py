import random
import discord
import asyncio
import aiohttp
import json


from discord import Game

from discord.ext.commands import Bot

BOT_PREFIX = "."

client = Bot (command_prefix=BOT_PREFIX)
client.remove_command('help')

client.run(os.getenv('TOKEN'))







@client.command(name='8ball')


async def eight_ball(context):

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
    await client.say(random.choice(possible_responses) + " " + context.message.author.mention)



@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('what'):
        await client.send_message(channel,'Whos your daddy?')




@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('fuck'):
        await client.send_message(channel,'Whos your daddy?')



@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('yeah'):
        await client.send_message(channel,'My Dog plays better than you')



@client.command(pass_context=True)
async def poke(ctx, member: discord.Member):
    await client.send_message(member, 'boop')




@client.command(pass_context=True)
async def help(ctx):
       embed = discord.Embed(title="How to get your tank added?", description=" DM GeneralSick#8995 to add your tank", color=0x4ec115)
       embed.add_field(name=".tanknamehere", value="Example: 'Tank_Name' not 'Tank Name'", inline=True)
       embed.add_field(name=".tpstat", value="Displays how many people are playing or waiting", inline=True)
       embed.add_field(name=".top25", value="Shows live list of current season leaderboard", inline =True)
       embed.add_field(name=".info @username", value="Information about discord user", inline=True)
       embed.add_field(name=".serverinfo", value="Server information", inline=True)
       embed.add_field(name=".help", value="displayes the help embed", inline=True)
       embed.add_field(name=".8ball", value="Answers from beyond...",inline=True)
       embed.add_field(name="Soon to come", value=".Calendar .Top25Global .addyourowntank .nexttourny", inline=True)
       embed.set_author(name="TankPit Bot help Use '.' to initiate command", icon_url='https://tankpit.com/images/icons/red_orb.png')
       embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
       embed.set_footer(text='https://tankpit.com')
       embed.set_image(url='https://tankpit.com/images/hero.png',)




       await client.say(embed=embed)



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

#****************************************************************************************************#
@client.command(name='Sick')
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
        rewards = response["awards"][0, 1]

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



@client.command(pass_context=True)
async def Grimlock(ctx):
        embed = discord.Embed(title="SERVICE RECORD: Grimlock", description="",  color =0x0000ff)
        url ='https://tankpit.com/api/tank?tank_id=968'
        response = requests.get(url).json()
        Bio = response["profile"]
        rewards = response["awards"]


        embed.add_field(name='Bio',value=Bio,inline=True)

        embed.add_field(name="Awards",value=rewards,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)


@client.command(name='The Strategist',
                description="Answers = a yes/no question.",
                brief="Answers from beyond.",
                pass_context=True)
async def adam(context):
        embed = discord.Embed(title="SERVICE RECORD: the Strategist", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=56595'
        response = requests.get(url).json()


        deac = response["map_data"]["World"]["deactivated"]
        time = response["map_data"]["World"]["time_played"]
        kills = response["map_data"]["World"]["destroyed_enemies"]
        ranks = response["map_data"]["World"]["rank"]

        embed.add_field(name="Deactivated", value=deac, inline=True)
        embed.add_field(name='Kills',value=kills,inline=True)
        embed.add_field(name='Time Played',value=time,inline=True)
        embed.add_field(name='Rank',value=ranks,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



#Pulled from top 100
@client.command(pass_context=True)
async def Homer_J_Simpson(ctx):
        embed = discord.Embed(title="SERVICE RECORD: Homer J Simpson", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=504'
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def noodle(ctx):
        embed = discord.Embed(title="SERVICE RECORD: noodle", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=25836'
        response = requests.get(url).json()
        deac = response["map_data"]["World"]["deactivated"]
        ranks = response["map_data"]["World"]["rank"]

        embed.add_field(name="Deactivated", value=deac, inline=True)
        embed.add_field(name='Rank',value=ranks,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def Dr_Hibbert(ctx):
        embed = discord.Embed(title="SERVICE RECORD: Dr Hibbert", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=25994'
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
        embed.add_field(name='Ping',value=pong,inline=True)
        embed.add_field(name='Time Played',value=favm,inline=True)
        embed.add_field(name='Rank',value=ranks,inline=True)
        embed.add_field(name='Country',value=location,inline=True)
        embed.add_field(name="Bio",value=profile,inline=True)
        embed.add_field(name="Awards",value=rewards,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def Incontinet_Beaver(ctx):
        embed = discord.Embed(title="SERVICE RECORD: Incontinent Beaver", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=4548'
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def BlueGhost(ctx):
        embed = discord.Embed(title="SERVICE RECORD: BlueGhost", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=539'
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)


@client.command(pass_context=True)
async def black_dragon(ctx):
        embed = discord.Embed(title="SERVICE RECORD: black dragont", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=8237'
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)


@client.command(pass_context=True)
async def a(ctx):
        embed = discord.Embed(title="SERVICE RECORD: ", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id='
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)




@client.command(pass_context=True)
async def aa(ctx):
        embed = discord.Embed(title="SERVICE RECORD: ", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id='
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)




@client.command(pass_context=True)
async def The_Dragon(ctx):
        embed = discord.Embed(title="SERVICE RECORD: The Dragon", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=45080'
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)


@client.command(pass_context=True)
async def aaa(ctx):
        embed = discord.Embed(title="SERVICE RECORD: ", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id='
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def aaaaa(ctx):
        embed = discord.Embed(title="SERVICE RECORD: ", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id='
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
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def ZIPPY(ctx):
        embed = discord.Embed(title="SERVICE RECORD: ZIPPY", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=59156'
        response = requests.get(url).json()
        deac = response["map_data"]["World"]["deactivated"]
        time = response["map_data"]["World"]["time_played"]
        kills = response["map_data"]["World"]["destroyed_enemies"]
        location = response["country"]
        favm = response["favorite_map"]
        rewards = response["awards"]

        embed.add_field(name="Deactivated", value=deac, inline=True)
        embed.add_field(name='Kills',value=kills,inline=True)
        embed.add_field(name='Time Played',value=time,inline=True)
        embed.add_field(name='Country',value=location,inline=True)
        embed.add_field(name="Awards",value=rewards,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)



@client.command(pass_context=True)
async def KAYNE(ctx):
        embed = discord.Embed(title="SERVICE RECORD: KAYNE", description="",  color =0xff0000)
        url ='https://tankpit.com/api/tank?tank_id=12590'
        response = requests.get(url).json()
        deac = response["map_data"]["World"]["deactivated"]
        time = response["map_data"]["World"]["time_played"]
        kills = response["map_data"]["World"]["destroyed_enemies"]
        location = response["country"]
        favm = response["favorite_map"]
        rewards = response["awards"]

        embed.add_field(name="Deactivated", value=deac, inline=True)
        embed.add_field(name='Kills',value=kills,inline=True)
        embed.add_field(name='Favorite map',value=favm,inline=True)
        embed.add_field(name='Time Played',value=time,inline=True)
        embed.add_field(name='Country',value=location,inline=True)
        embed.add_field(name="Awards",value=rewards,inline=True)
        embed.set_author(name="TankPit Stats",icon_url='https://tankpit.com/images/icons/red_orb.png')
        embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
        embed.set_footer(text='https://tankpit.com')
        await client.say(embed=embed)


        
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



@client.command(pass_context=True)
async def site1():
    embed = discord.Embed(title="Enjin Communities", description="Site 320189",  color =0x00e100)
    page= requests.get("https://hypedgamingonline.enjin.com/page/320189")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(id="section-main")
    Sitename = data("h1")[0].get_text()
    about = data("div")[39].get_text()
    members = data("a")[7].get_text()
    sitehits =data("span")[2].get_text()

    embed.add_field(name="Community Name", value=Sitename, inline=True)
    embed.add_field(name="Community description", value=about, inline=True)
    embed.add_field(name="Site Members", value=members, inline=True)
    embed.add_field(name="Site Hits", value=sitehits, inline=True)
    embed.set_image(url='https://i.imgur.com/uYAWXqZ.png')
    embed.set_thumbnail(url='http://i42.photobucket.com/albums/e310/TravisClarkakaTc/titleimagepng_zps5a484315.png')
    embed.set_author(name="Enjin Site Stats by Zephireis#8995",icon_url='http://esportsobserver.com/wp-content/uploads/2015/05/enjin_logo_squared.png')
    embed.set_footer(text='Website powered by Enjin')
    await client.say(embed=embed)



    
client.run(TOKEN)
