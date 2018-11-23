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



TOKEN = "MjcxMzcwODc3NzAxMDYyNjY3.DlVh3Q.RUA6UwA24OLcR5O1JCOwBGa0wpY"
BOT_PREFIX = ".","?"


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')


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
       embed = discord.Embed(title=' ', description='Prefix: .', color=0x4ec115)
       embed.add_field(name="TankPit Commands", value="``activity``,``top25``,``tp``,``id``", inline=True)
       embed.add_field(name="General Commands", value="``help``,``info``,``8ball``,``serverinfo``", inline=False)
       embed.set_author(name="TankPit Command List", icon_url='https://tankpit.com/images/icons/red_orb.png')
       embed.set_thumbnail(url='https://tankpit.com/images/icons/green.png')
       embed.set_image(url='https://tankpit.com/images/hero.png',)
       embed.set_footer(text='To get tank stats set your tank stats to public')

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

@client.command()
async def tpa(tank_name):

    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/find_tank?name=' + tank_name)
        resp_json = await response.json()


        awards_dict = {0: '', 1: '🙃', 2: '🤣', 3: '😃'}# set one through three for value 1 in json
        awards_string = ''
        for awards in resp_json[0]["awards"][0:1]:
            awards_string += awards_dict.get(awards,'' )
        await client.say(awards_string)




def award_string(seq: list) -> str:
    emoji_set = [
        ['','<:S_Star_New:476303220570849301>','<:D_Star_New:476303233640431617>','<:T_Star_new:476303253794062348>'],
        ['','<:tankb2:476998057595240469>','<:tanks2:476997284878483466>','<:tankg2:476996100377804802>'],
        ['','<:C_Honor_New:476303395288776705>','<:B_Honor_New:476303426985132053>','<:H_Honor_New:476303438142111746>'],
        ['','<:S_Sword_New:476303643411349514>','<:B_Sword_New:476303654916194304>','<:R_Sword_New:476303669823012875>'],
        ['','', '','<:DoT_New:476303764580597761>'],
        ['', '<:B_Cup_New:476303841562853377>','<:S_Cup_New:476303857924833290>','<:G_Cup_New:476303868486221824>'],
        ['','<:PH_New:476303889143037952>','<:PH_New:476303889143037952>','<:PH_New:476303889143037952>'],
        ['','<:WC_New:476303897737297931>','',''],
        ['','<:LB_New:476303919870640130>','',''],
    ]
    if len(seq) != 9:
        raise Exception('Invalid Length')
    awards = [emoji_set[i][award] for i,award in enumerate(seq)]
    return ''.join(awards)
@client.command()
async def tp(tank_name):
    embed = discord.Embed(title="", description="", color=0x00ff00)
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/find_tank?name=' + tank_name)
        resp_json = await response.json()
        ids = resp_json[0]['tank_id']
        awards = award_string(resp_json[0]['awards'])
        embed.add_field(name="Tank", value=resp_json[0]['name'], inline=True)
        embed.add_field(name="Awards", value=f'{awards}'"\u200b", inline=True)
        embed.add_field(name="Unit ID", value=resp_json[0]['tank_id'], inline=False)
        embed.set_footer(text='use command .id'f' {ids}'' for indepth tank stats')
        await client.say(embed=embed)




@client.command()
async def id(tank_id):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/tank?tank_id=' + tank_id )
        resp = await response.json()
        awards1 = award_string(resp['awards'])
        tptank2 = resp.get("name", "N/A")
        embed = discord.Embed(title="SERVICE RECORD: " + f'{tptank2}', description="",  color =0xdd3d20)
        try:
            time = resp["map_data"]["World"]["time_played"]
            ranks = resp["map_data"]["World"]["rank"]
            kills = resp["map_data"]["World"]["destroyed_enemies"]
            deac = resp ["map_data"]["World"]["deactivated"]
        except:
            await client.say("```VALUE ERROR: 'World' stats not public```")


        lastplayed =  resp.get("last_played", "\u200b")
        favm = resp.get("favorite_map", "\u200b")
        bftank= resp.get("bf_tank_name", "\u200b")
        pong = resp.get("ping", "\u200b")
        location = resp.get("country", "\u200b")
        Bio = resp.get("profile", "\u200b")
        tptank = resp.get("name", "\u200b")
        space ="\u200b"

        embed.add_field(name='Name', value=f'{tptank}'f'{space}', inline=True)
        try:
            embed.add_field(name="Time Played", value=f'{time}'f'{space}', inline=True)
        except:
            embed.add_field(name="Time Played", value="\u200b", inline=True)
        try:
            embed.add_field(name="Rank", value=f'{ranks}'f'{space}', inline=True)
        except:
            embed.add_field(name="Rank", value=f'\u200b', inline=True)
        try:
            embed.add_field(name="Kills", value=f'{kills}'f'{space}', inline=True)
        except:
            embed.add_field(name="Kills", value='\u200b', inline=True)
        try:
            embed.add_field(name="Deaths", value=f'{deac}'f'{space}', inline=True)
        except:
            embed.add_field(name="Deaths", value='\u200b', inline=True)
        embed.add_field(name="Last Played", value=f'{lastplayed}'f'{space}', inline=True)
        embed.add_field(name="Favorite Map", value=f'{favm}'f'{space}', inline=True)
        embed.add_field(name="BattleField Tank", value=f'{bftank}'f'{space}', inline=True)
        embed.add_field(name="Ping", value=f'{pong}'f'{space}', inline=True)
        embed.add_field(name="Country", value=f'{location}'f'{space}', inline=True)
        embed.add_field(name="Bio", value=f'{Bio}'f'{space}', inline=False)
        try:
            embed.add_field(name="Awards", value=f'{awards1}'f'{space}', inline=False)
        except:
            embed.add_field(name="Awards", value='\u200b', inline=False)
        await client.say(embed=embed)















#-------INSTALLATION 01-------------
@client.command(pass_context=True)
async def i01():
    embed = discord.Embed(title="INSTALLATION 01 STATS", url="https://installation01.org/soon",  color =0xdd3d20)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/989667244929044480/byfkjFPt_400x400.jpg")
    page= requests.get("https://installation01.org/")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find("a", {"class": "box"})
    spartans = data()[4].get_text()
    games = data()[7].get_text()
    allspartans = data()[10].get_text()
    allgame =data()[13].get_text()

    embed.add_field(name="Spartans (24hr)", value=spartans, inline=True)
    embed.add_field(name="Games (24hr)", value=games, inline=True)
    embed.add_field(name="Spartans(All Time)", value=allspartans, inline=True)
    embed.add_field(name="Games(All Time)", value=allgame, inline=True)
    embed.set_image(url='https://static.i01.co/blog/NewOrderConcept.jpg',)
    await client.say(embed=embed)




@client.command(pass_context=True)
async def ed():
    embed = discord.Embed(title="Eldewrito Stats", url="https://pre00.deviantart.net/e7f6/th/pre/f/2015/150/c/a/eldewrito_logo_blue_by_floodgrunt-d8vd5q5.png", color =0xdd3d20)
    page = requests.get("http://halostats.click/leaderboard")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_="row")
    games = data("div").get_text()


    embed.add_field(name="Ranked", value=data, inline=True)
    await client.say(embed=embed)



#------TANKPITHQ----------
@client.command(pass_context=True)#this works with class
async def hq():
    embed = discord.Embed(title="Eldewrito Stats", url="https://pre00.deviantart.net/e7f6/th/pre/f/2015/150/c/a/eldewrito_logo_blue_by_floodgrunt-d8vd5q5.png", color =0xdd3d20)
    page = requests.get("https://tankpithq.enjin.com/profile/zephireis")
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_="widget_tags_awards")
    activity = data("div")[0].get_text()



embed = discord.Embed(title="Top25 Current season (Live updates)", description="",  color =0x00e100)
page= requests.get("https://tankpit.com/top25")
soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find(id="top25-page")




#----------tankpit site stats commands---------
@client.command(pass_context=True)
async def acti():
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





@client.command()
async def activity():
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/active_games')
        resp = await response.json()
        map1=resp[1]['map']
        players=resp[1]['playing_tanks']
        Name=resp[1]["name"]
        map0=resp[0]['map']
        players0=resp[0]['playing_tanks']
        id=resp[1]['name']
        MINIMAP = {
        'World (Rocks and Swamp)': 'https://tankpit.com/images/maps/field01.gif',
        'World (The Nile)': 'https://tankpit.com/images/maps/field13.gif',
        'World (Crazy Maze)': 'https://tankpit.com/images/maps/field02.gif',
        'World (Appaloosa land)': 'https://tankpit.com/images/maps/field03.gif',
        'World (Castles)': 'https://tankpit.com/images/maps/field04.gif',
        'World (Desert)': 'https://tankpit.com/images/maps/field05.gif',
        'World (Iceland)': 'https://tankpit.com/images/maps/field06.gif',
        'World (Deep Six)': 'https://tankpit.com/images/maps/field07.gif',
        'World (Levels)': 'https://tankpit.com/images/maps/field08.gif',
        'World (Metropolis)': 'https://tankpit.com/images/maps/field09.gif',
        'World (Elements)': 'https://tankpit.com/images/maps/field21.gif',
        'World (Orbital)': 'https://tankpit.com/images/maps/field23.gif',
        }
        id = MINIMAP[id]


        embed = discord.Embed(title="Active Games", description="Current players in game",  color =0xdd3d20)
        embed.set_thumbnail(url=f'{id}')
        embed.add_field(name=f'{Name}', value=f'{map1}', inline=True)
        embed.add_field(name="Players", value=resp[1]['playing_tanks'], inline=True)
        embed.add_field(name="Waiting Players", value=resp[0]['waiting_tanks'], inline=True)
        await client.say(embed=embed)



@client.command()
async def ntourny():
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/upcoming_tournaments')
        resp = await response.json()
        embed = discord.Embed(title="Upcoming Tournaments", description="",  color =0xdd3d20)
        embed.add_field(name="Start Time", value=resp[0]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[0]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[0]['map'], inline=True)
        embed.add_field(name="Start Time", value=resp[1]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[1]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[1]['map'], inline=True)
        embed.add_field(name="Start Time", value=resp[2]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[2]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[2]['map'], inline=True)
        embed.add_field(name="Start Time", value=resp[3]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[3]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[3]['map'], inline=True)
        embed.add_field(name="Start Time", value=resp[4]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[4]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[4]['map'], inline=True)
        embed.add_field(name="Start Time", value=resp[5]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[5]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[5]['map'], inline=True)
        await client.say(embed=embed)



@client.command()
async def results(id):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/tournament_results?tournament_id=' + id)
        resp = await response.json()
        date = resp["start_time_utc"]
        place0 = resp["results"][0]["placing"]
        place1 = resp["results"][1]["placing"]
        place2 = resp["results"][2]["placing"]
        place3 = resp["results"][3]["placing"]
        place4 = resp["results"][4]["placing"]
        place5 = resp["results"][5]["placing"]
        place6 = resp["results"][6]["placing"]
        place7 = resp["results"][7]["placing"]
        place8 = resp["results"][8]["placing"]
        place9 = resp["results"][9]["placing"]
        place10 = resp["results"][10]["placing"]
        place11 = resp["results"][11]["placing"]
        place12 = resp["results"][12]["placing"]
        place13 = resp["results"][13]["placing"]
        place14 = resp["results"][14]["placing"]
        name0 = resp["results"][0]["name"]
        name1 = resp["results"][1]['name']
        name2 = resp["results"][2]['name']
        name3 = resp["results"][3]['name']
        name4 = resp["results"][4]['name']
        name5 = resp["results"][5]['name']
        name6 = resp["results"][6]['name']
        name7 = resp["results"][7]['name']
        name8 = resp["results"][8]['name']
        name9 = resp["results"][9]['name']
        name10 = resp["results"][10]['name']
        name11 = resp["results"][11]['name']
        name12 = resp["results"][12]['name']
        name13 = resp["results"][13]['name']
        name14 = resp["results"][14]['name']
        rank0 = resp["results"][0]['rank']
        rank1 = resp["results"][1]['rank']
        rank2 = resp["results"][2]['rank']
        rank3 = resp["results"][3]['rank']
        rank4 = resp["results"][4]['rank']
        rank5 = resp["results"][5]['rank']
        rank6 = resp["results"][6]['rank']
        rank7 = resp["results"][7]['rank']
        rank8 = resp["results"][8]['rank']
        rank9 = resp["results"][9]['rank']
        rank10 = resp["results"][10]['rank']
        rank11 = resp["results"][11]['rank']
        rank12 = resp["results"][12]['rank']
        rank13= resp["results"][13]['rank']
        rank14 = resp["results"][14]['rank']
        space ="\u200b"
        awards0 = award_string(resp['results'][0]['awards'])
        awards1 = award_string(resp['results'][1]['awards'])
        awards2 = award_string(resp['results'][2]['awards'])
        awards3 = award_string(resp['results'][3]['awards'])
        awards4 = award_string(resp['results'][4]['awards'])
        awards5 = award_string(resp['results'][5]['awards'])
        awards6 = award_string(resp['results'][6]['awards'])
        awards7 = award_string(resp['results'][7]['awards'])
        awards8 = award_string(resp['results'][8]['awards'])
        awards9 = award_string(resp['results'][9]['awards'])
        awards10 = award_string(resp['results'][10]['awards'])
        awards11 = award_string(resp['results'][11]['awards'])
        awards12 = award_string(resp['results'][12]['awards'])
        awards13 = award_string(resp['results'][13]['awards'])
        awards14 = award_string(resp['results'][14]['awards'])
        none ="‍▪️"

        embed = discord.Embed(title="Tournament Results " + f'{date}', description="",  color =0xdd3d20)
        embed.add_field(name="Placing""", value='#'f'``{place0}``'' 'f'**{name0}**'f'{awards0}'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place1}``'' 'f'**{name1}**'f'{awards1}'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place2}``'' 'f'**{name2}**'f'{awards2}'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place4}``'' 'f'**{name3}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place5}``'' 'f'**{name4}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place6}``'' 'f'**{name5}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place7}``'' 'f'**{name6}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place8}``'' 'f'**{name7}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place9}``'' 'f'**{name8}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place10}``'' 'f'**{name9}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place11}``'' 'f'**{name10}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place12}``'' 'f'**{name11}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place13}``'' 'f'**{name12}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place13}``'' 'f'**{name13}**'"\n"f'{space}'' 'f'{space}'"\n"
        '#'f'``{place14}``'' 'f'**{name14}**'f"\n"f'{space}'' 'f'{space}'"\n", inline=True)#mark
        embed.add_field(name='Rank', value=f'{rank0}')
        await client.say(embed=embed)


@client.command()
async def bb(id):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/bb/post?post_id=' + id)
        resp = await response.json()
        sec = resp["section"]
        space ="\u200b"
        name = resp["tank_name"]
        message = resp["message"]
        Month = resp["month"]
        Day = resp["day"]
        Year = resp["year"]
        awards = award_string(resp['awards'])

        embed = discord.Embed(title="", description="",  color =0xdd3d20)
        embed.set_author(name="TankPit Bulletin Board Post: "f'{Month}'"/"f'{Day}'"/"f'{Year}', url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name=f'{space}', value=f'```{sec}```', inline=True)
        embed.add_field(name=f'{space}', value=f'{message}',inline=True)
        embed.add_field(name=f'{space}', value="-"f'{name}'" "f'{awards}',inline=False)


        await client.say(embed=embed)


@client.command()
async def bbb(year,month,day):
    async with aiohttp.ClientSession()as session:
        a="&"
        year=[2018]
        month=[8]
        day=[12]
        response = await session.get('https://tankpit.com/api/bb/?year='+f'{year}'f'{month}'f'{day}')
        resp = await response.json()
        name = resp[0]["tank_name"]
        embed = discord.Embed(title="", description="",  color =0xdd3d20)
        embed.add_field(name="test", value=f'{name}', inline=True)
        await client.say(embed=embed)









@client.command(pass_context=True)
async def top25():
    embed = discord.Embed(title="Top25 Current season (Live updates)", description="", url="https://tankpit.com/top25",  color =0x00e100)
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
    embed.add_field(name="TankPit Bot Commands", value="``help``, ``8ball``, ``tankhere``, ``serverinfo``, ``info@username``, ``activity``, ``top25``, ``tp``,``id``", inline=True)
    await client.send_message(member, embed=embed)
    channel = discord.utils.get(member.server.channels, name="general")
    embed=discord.Embed(title="Has entered the field", description=" ",  color =0x389b2b)
    message = '{}'.format(member.mention)
    await client.send_message(channel, message, embed=embed)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '.alertson':
        role = discord.utils.get(message.server.roles, name='Active Duty')
        await client.add_roles(message.author, role)
    if message.author == client.user:
        return
    if message.content == '.alertsoff':
        role = discord.utils.get(message.server.roles, name='Active Duty')
        await client.remove_roles(message.author, role)
    await client.process_commands(message)

@client.command(name='alertson')
async def alerts_on():
    embed=discord.Embed(title="Alerts have been enabled 🔊", description="",  color =0x7d2789)
    await client.say(embed=embed)

@client.command(name='alertsoff')
async def alerts_off():
    embed=discord.Embed(title="Alerts have been disabled 🔇", description="",  color =0x7d2789)
    await client.say(embed=embed)









#-----MODERATION-----------------------
@client.command(pass_context=True)
async def clear(ctx, amount=1):
    if ctx.message.author.server_permissions.manage_messages:
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say("Messages deleted")






@client.event
async def on_member_remove(member):
    embed=discord.Embed(title="Has left the field", description="",  color =0x7d2789)
    server = member.server
    channel = discord.utils.get(member.server.channels, name="general")
    message = '{}'.format(member.mention)
    await client.send_message(channel, message, embed=embed)

#-----Bot Status-----------------------




@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Type: ?help"))
    print("logged in as" + client.user.name)




client.run(TOKEN)
