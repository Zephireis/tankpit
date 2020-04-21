import random
import discord
import asyncio
import aiohttp
import requests
import json
import html5lib
import os
import asyncio
import threading
import sqlite3
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials



from discord import Game
from bs4 import BeautifulSoup
from discord.ext.commands import Bot



TOKEN = "MjcxMzcwODc3NzAxMDYyNjY3.D0c35A.EQYFgFoWeKtyXs5PN5ZatKdSHSc"
BOT_PREFIX = ".","?"


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("usertanks-301e55f761c4.json", scope)
creds.refresh 
Client = gspread.authorize(creds)

def getCell(sheet, r, c, sheetName='profile'):
    client.login()
    try:
        return client.open(sheetName).get_worksheet(sheet).cell(r,c).value      #Actual Action
        #print(action)
    except Exception as e:
        print(e)
        #client.login() (here better?)
        getCell(sheet, r, c, sheetName)


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
       embed.add_field(name="TankPit Commands", value="``.tp`` ``.prf`` ``.report`` ``.id`` ``.tourny`` ``.results`` ``.bb`` ``.pst`` ``.season``", inline=True)
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

@client.command(pass_context=True)
async def create(ctx, file):
    f= open(f'{file}.db',"w+")
    await client.say(f"Team ``{file}`` was created".format(ctx.message.author.mention))
    await client.say(f"add members by using ``.add {file} player.``\nto see roster use ``.roster teamname``")


@client.command()
async def add(team, tank):
    connection = sqlite3.connect(f'{team}.db')
    cursor = connection.cursor()

    cursor.execute(f'CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute('INSERT INTO names(name) VALUES(?)', (f'{tank}', ))
    await client.say(f'{tank} added to team roster')

    connection.commit()

@client.command()
async def roster(clan):
    embed = discord.Embed(title="", description="", color=0x00ff00)
    connection = sqlite3.connect(f'{clan}.db')

    cursor = connection.cursor()

    names = [name[0] for name in cursor.execute("SELECT name FROM names")]
    await client.say(names)







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
@client.command(pass_context=True)
async def tp(ctx, tank:str):
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/find_tank?name={tank}')
        await asyncio.sleep(2)
        resp_json = await response.json()
        ids = resp_json[0]['tank_id']
        NAME = resp_json[0]['name']
        awards = award_string(resp_json[0]['awards'])
        embed = discord.Embed(title=f'{NAME} {awards}', description="", color=0x18e728)
        embed.set_footer(text='use command .id'f' {ids}'' for indepth tank stats')
    async with aiohttp.ClientSession()as sess:
        respons = await sess.get(f'https://tankpit.com/api/tank?tank_id={ids}')
        resp = await respons.json()
        try:
            time = resp["map_data"]["World"]["time_played"]
        except:
            embed.set_footer(text="Players 'World' Stats 'time played' not set to public")
        try:
            ranks = resp["map_data"]["World"]["rank"]
        except:
            embed.set_footer(text="Players 'World' Stats 'rank' not set to public")
        try:
            kills = resp["map_data"]["World"]["destroyed_enemies"]
        except:
            embed.set_footer(text="Players 'World' Stats 'kills' not set to public")
        try:
            deac = resp ["map_data"]["World"]["deactivated"]
        except:
            embed.set_footer(text="Players 'World' Stats 'deactivated' not set to public")


        lastplayed =  resp.get("last_played", "\u200b")
        favm = resp.get("favorite_map", "\u200b")
        bftank= resp.get("bf_tank_name", "\u200b")
        pong = resp.get("ping", "\u200b")
        location = resp.get("country", "\u200b")
        Bio = resp.get("profile", "\u200b")
        tptank = resp.get("name", "\u200b")
        space ="\u200b"

        try:
            cups = resp['user_tournament_victories'] ['bronze']
        except KeyError:
            a = "<:B_Cup_New:476303841562853377>x0"
        try:
            cups1 = resp['user_tournament_victories'] ['silver']
        except:
            b= "<:S_Cup_New:476303857924833290>x0"
        try:
            cups2 = resp['user_tournament_victories'] ['gold']
        except:
            c = "<:G_Cup_New:476303868486221824>x0"

        try:
            embed.add_field(name="Time Played", value=f'{time}{space}', inline=True)
        except:
            embed.add_field(name="Time Played", value="\u200b", inline=True)
        try:
            embed.add_field(name="Rank", value=f'{ranks}{space}', inline=True)
        except:
            embed.add_field(name="Rank", value=f'\u200b', inline=True)
        try:
            embed.add_field(name="Kills", value=f'{kills}{space}', inline=True)
        except:
            embed.add_field(name="Kills", value='\u200b', inline=True)
        try:
            embed.add_field(name="Deaths", value=f'{deac}{space}', inline=True)
        except:
            embed.add_field(name="Deaths", value='\u200b', inline=True)
        try:
            embed.add_field(name="Cups", value=f'<:B_Cup_New:476303841562853377>x{cups}<:S_Cup_New:476303857924833290>x{cups1}<:G_Cup_New:476303868486221824>x{cups2}{space}', inline=True)
        except:
            embed.add_field(name="Cups", value=f"{a}{b}{c}", inline=True)

        embed.add_field(name="Last played", value=resp.get("last_played", "\u200b"), inline=True)

        await client.say(embed=embed)


@client.command(pass_context=True)
async def prf(ctx, tank):
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/find_tank?name={tank}')
        resp_json = await response.json()
        ids = resp_json[0]['tank_id']
        NAME0 = resp_json[0]['name']
        awards0 = award_string(resp_json[0]['awards'])
        space ="\u200b"
        embed = discord.Embed(title=f"Top 5 of {NAME0}", description="", color=0x00ff00)
        embed.add_field(name=f'{NAME0}\n{awards0}', value=f"{space}", inline=True)



        page= requests.get(f"https://tankpit.com/tank_profile/?tank_id={ids}")
        soup = BeautifulSoup(page.content, 'html.parser')
    try:
        tank1 = soup.find_all('b')[1].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    try:
        tank2 = soup.find_all('b')[2].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    try:
        tank3 = soup.find_all('b')[3].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    try:
        tank4 = soup.find_all('b')[4].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    try:
        tank5 = soup.find_all('b')[5].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    try:
        tank6 = soup.find_all('b')[6].get_text()
    except IndexError:
        await client.say(f"Player {tank} has not enabled top 5 tanks on site profile (5 tanks required for command)")
        return
    async with aiohttp.ClientSession()as session1:
        response1 = await session1.get(f'https://tankpit.com/api/find_tank?name={tank1}')
        resp_json1 = await response1.json()
        id1 = resp_json1[0]['tank_id']
        NAME1 = resp_json1[0]['name']
        awards1 = award_string(resp_json1[0]['awards'])
        embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=True)
    async with aiohttp.ClientSession()as session2:
        response2 = await session2.get(f'https://tankpit.com/api/find_tank?name={tank2}')
        resp_json2 = await response2.json()
        id2 = resp_json2[0]['tank_id']
        NAME2 = resp_json2[0]['name']
        awards2 = award_string(resp_json2[0]['awards'])
        embed.add_field(name=f'{NAME2}\n{awards2}', value=f"{space}", inline=True)
    async with aiohttp.ClientSession()as session3:
        response3 = await session3.get(f'https://tankpit.com/api/find_tank?name={tank3}')
        resp_json3 = await response3.json()
        id3 = resp_json3[0]['tank_id']
        NAME3 = resp_json3[0]['name']
        awards3 = award_string(resp_json3[0]['awards'])
        embed.add_field(name=f'{NAME3}\n{awards3}', value=f"{space}", inline=True)
    async with aiohttp.ClientSession()as session4:
        response4 = await session4.get(f'https://tankpit.com/api/find_tank?name={tank4}')
        resp_json4 = await response4.json()
        id4 = resp_json4[0]['tank_id']
        NAME4 = resp_json4[0]['name']
        awards4 = award_string(resp_json4[0]['awards'])
        embed.add_field(name=f'{NAME4}\n{awards4}', value=f"{space}", inline=True)
    async with aiohttp.ClientSession()as session5:
        response5 = await session5.get(f'https://tankpit.com/api/find_tank?name={tank5}')
        resp_json5 = await response5.json()
        id5 = resp_json5[0]['tank_id']
        NAME5 = resp_json5[0]['name']
        awards5 = award_string(resp_json5[0]['awards'])
        embed.add_field(name=f'{NAME5}\n{awards5}', value=f"{space}", inline=True)
        await client.say(embed=embed)


@client.command(pass_context = True)
async def report(ctx,user:discord.User,*reason:str):
  embed = discord.Embed(title="", description="User Reports",  color =0xdd3d20)
  embed.add_field(name=f'{user}', value=f'{reason}', inline=True)
  await client.send_message(discord.Object(id='553833349651628052'), embed=embed)
  if not reason:
    await client.say("Please provide a reason")
    return
  reason = ' '.join(reason)

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
async def activity(): # NOTE: NEEDS FIXED
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/active_games')
        resp = await response.json()
        map1=resp[0]['map']
        players=resp[1]['playing_tanks']
        Name=resp[0]["name"]
        map0=resp[1]['map']
        players0=resp[1]['playing_tanks']
        id=resp[0]['name']
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
        embed.add_field(name=f'{Name}', value=f'{map0}', inline=True)
        embed.add_field(name="Players", value=resp[0]['playing_tanks'], inline=True)
        embed.add_field(name="Practice", value=resp[1]['map'], inline=True)
        embed.add_field(name="Players", value=resp[1]['playing_tanks'], inline=True)
        embed.add_field(name="Waiting Players", value=resp[1]['waiting_tanks'], inline=True)
        await client.say(embed=embed)



@client.command()
async def tourny():
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/upcoming_tournaments')
        resp = await response.json()
        embed = discord.Embed(title="Upcoming Tournaments", description="",  color =0xdd3d20)
        embed.add_field(name="Start Time", value=resp[0]['start_time_utc'], inline=True)
        embed.add_field(name="End Time", value=resp[0]['end_time_utc'], inline=True)
        embed.add_field(name="Map", value=resp[0]['map'], inline=True)
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
        color0 = resp['results'][0]["color"]
        color1 = resp['results'][1]["color"]
        color2 = resp['results'][2]["color"]
        color3 = resp['results'][3]["color"]
        color4 = resp['results'][4]["color"]
        color5 = resp['results'][5]["color"]
        color6 = resp['results'][6]["color"]
        color7 = resp['results'][7]["color"]
        color8 = resp['results'][8]["color"]
        color9 = resp['results'][9]["color"]
        color10 = resp['results'][10]["color"]
        COLORS = {
        'red': '<:r_:524455235188424718>',
        'blue': '<:b_:480148438487531520>',
        'purple': '<:p_:524458234803650580>',
        'orange': '<:o_:524458234694860800>',
        }
        color0 = COLORS[color0]
        color1 = COLORS[color1]
        color2 = COLORS[color2]
        color3 = COLORS[color3]
        color4 = COLORS[color4]
        color5 = COLORS[color5]
        color6 = COLORS[color6]
        color7 = COLORS[color7]
        color8 = COLORS[color8]
        color9 = COLORS[color9]
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

        none ="???"

        embed = discord.Embed(title="Tournament Results " + f'{date}', description="",  color =0xdd3d20)
        embed.add_field(name=f"{space}", value=f"1 {color0}  {name0}{awards0}\n2 {color1}  {name1}{awards1}\n3 {color2}  {name2}{awards2}\n4 {color3}  {name3}\n5 {color4}  {name4}\n6 {color5}  {name5}\n7 {color6}  {name6}\n8 {color7}  {name7}\n9 {color8}  {name8}\n10{color9}  {name9}", inline=False)

        await client.say(embed=embed)


@client.command()
async def bb(year, month, day):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/bb?year='f'{year}&month={month}&day={day}')
        resp = await response.json()
        awards0 = award_string(resp[0]['awards'])
        embed = discord.Embed(title="TankPit BulletinBoard 📖", description= "",  color =0xdd3d20)

        try:
            awards0 = award_string(resp[0]['awards'])
            tank = resp[0]["tank_name"]
            message0 = resp[0]["message"]
            embed.add_field(name="\u200b", value=f'{message0}\n**{tank}** {awards0}', inline=True)
        except:
            print("m0 none")
        try:
            s1 = resp[1]["section"]
            awards1 = award_string(resp[1]['awards'])
            tank1 = resp[1]["tank_name"]
            message1 = resp[1]["message"]
            embed.add_field(name="\u200b", value=f'{message1}\n**{tank1}** {awards1}', inline=True)
        except:
            print("m1 none")
        try:
            s2 = resp[2]["section"]
            awards2 = award_string(resp[2]['awards'])
            tank2 = resp[2]["tank_name"]
            message2 = resp[2]["message"]
            embed.add_field(name="\u200b", value=f'{message2}\n**{tank2}** {awards2}', inline=True)
        except:
            print("m2 none")
        try:
            s3 = resp[2]["section"]
            awards3 = award_string(resp[3]['awards'])
            tank3 = resp[3]["tank_name"]
            message3 = resp[3]["message"]
            embed.add_field(name="\u200b", value=f'{message3}\n**{tank3}** {awards3}', inline=True)
        except:
            print("m3 None")
        try:
            awards4 = award_string(resp[4]['awards'])
            tank4 = resp[4]["tank_name"]
            message4 = resp[4]["message"]
            embed.add_field(name="\u200b", value=f'{message4}\n**{tank4}** {awards4}', inline=True)
        except:
            print("m4 None")
        try:
            awards5 = award_string(resp[5]['awards'])
            tank5 = resp[5]["tank_name"]
            message5 = resp[5]["message"]
            embed.add_field(name="\u200b", value=f'{message5}\n**{tank5}** {awards5}', inline=True)
        except:
            print("m5 None")
        try:
            awards6 = award_string(resp[6]['awards'])
            tank6 = resp[6]["tank_name"]
            message6 = resp[6]["message"]
            embed.add_field(name="\u200b", value=f'{message6}\n**{tank6}** {awards6}', inline=True)
        except:
            print("m6 None")
        try:
            awards7 = award_string(resp[7]['awards'])
            tank7 = resp[7]["tank_name"]
            message7 = resp[7]["message"]
            embed.add_field(name="\u200b", value=f'{message7}\n**{tank7}** {awards7}', inline=True)
        except:
            print("m7 None")
        try:
            awards8 = award_string(resp[8]['awards'])
            tank8 = resp[8]["tank_name"]
            message8 = resp[8]["message"]
            embed.add_field(name="\u200b", value=f'{message8}\n**{tank8}** {awards8}', inline=True)
        except:
            print("m8 None")
        try:
            awards9 = award_string(resp[9]['awards'])
            tank9 = resp[9]["tank_name"]
            message9 = resp[9]["message"]
            embed.add_field(name="\u200b", value=f'{message9}\n**{tank9}** {awards9}', inline=True)
        except:
            print("m9 None")
        try:
            awards10 = award_string(resp[10]['awards'])
            tank10 = resp[10]["tank_name"]
            message10 = resp[10]["message"]
            embed.add_field(name="\u200b", value=f'{message10}\n**{tank10}** {awards10}', inline=True)
        except:
            print("m10 None")
        try:
            awards11 = award_string(resp[11]['awards'])
            tank11 = resp[11]["tank_name"]
            message11 = resp[11]["message"]
            embed.add_field(name="\u200b", value=f'{message11}\n**{tank11}** {awards11}', inline=True)
        except:
            print("m11 None")
        try:
            awards12 = award_string(resp[12]['awards'])
            tank12 = resp[12]["tank_name"]
            message12 = resp[12]["message"]
            embed.add_field(name="\u200b", value=f'{message12}\n**{tank12}** {awards12}', inline=True)
        except:
            print("m12 None")
        try:
            awards13 = award_string(resp[13]['awards'])
            tank13 = resp[13]["tank_name"]
            message13 = resp[13]["message"]
            embed.add_field(name="\u200b", value=f'{message13}\n**{tank13}** {awards13}', inline=True)
        except:
            print("m13 None")
        await client.say(embed=embed)

@client.command()
async def season(year):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/leaderboards/'+year)
        resp = await response.json()
        space ="\u200b"
        leader= resp["leaderboard"]
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
        tank0 = resp["results"][0]["name"]
        tank1 = resp["results"][1]["name"]
        tank2 = resp["results"][2]["name"]
        tank3 = resp["results"][3]["name"]
        tank4 = resp["results"][4]["name"]
        tank5 = resp["results"][5]["name"]
        tank6 = resp["results"][6]["name"]
        tank7 = resp["results"][7]["name"]
        tank8 = resp["results"][8]["name"]
        tank9 = resp["results"][9]["name"]
        tank10 = resp["results"][10]["name"]
        color0 = resp['results'][0]["color"]
        color1 = resp['results'][1]["color"]
        color2 = resp['results'][2]["color"]
        color3 = resp['results'][3]["color"]
        color4 = resp['results'][4]["color"]
        color5 = resp['results'][5]["color"]
        color6 = resp['results'][6]["color"]
        color7 = resp['results'][7]["color"]
        color8 = resp['results'][8]["color"]
        color9 = resp['results'][9]["color"]
        color10 = resp['results'][10]["color"]
        place0 = resp['results'][0]["placing"]
        place1 = resp['results'][1]["placing"]
        place2 = resp['results'][2]["placing"]
        place3 = resp['results'][3]["placing"]
        place4 = resp['results'][4]["placing"]
        place5 = resp['results'][5]["placing"]
        place6 = resp['results'][6]["placing"]
        place7 = resp['results'][7]["placing"]
        place8 = resp['results'][8]["placing"]
        place9 = resp['results'][9]["placing"]
        place10 = resp['results'][10]["placing"]
        COLORS = {
        'red': '<:r_:524455235188424718>',
        'blue': '<:b_:480148438487531520>',
        'purple': '<:p_:524458234803650580>',
        'orange': '<:o_:524458234694860800>',
        }
        color0 = COLORS[color0]
        color1 = COLORS[color1]
        color2 = COLORS[color2]
        color3 = COLORS[color3]
        color4 = COLORS[color4]
        color5 = COLORS[color5]
        color6 = COLORS[color6]
        color7 = COLORS[color7]
        color8 = COLORS[color8]
        color9 = COLORS[color9]
        embed = discord.Embed(title="Season"+" "f'{leader}', description="",  color =0xdd3d20)
        embed.set_author(name="TankPit Leaderboards", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_thumbnail(url="https://tankpit.com/images/icons/classy.png")
        embed.add_field(name="1 "f'{color0}  {tank0}{awards0}', value="2 "f'{color1}  {tank1}{awards1}', inline=False)
        embed.add_field(name="3 "f'{color2}  {tank2}{awards2}', value="4 "f'{color3}  {tank3}{awards3}', inline=False)
        embed.add_field(name="5 "f'{color4}  {tank4}{awards4}', value="6 "f'{color5}  {tank5}{awards5}', inline=False)
        embed.add_field(name="7 "f'{color6}  {tank6}{awards6}', value="8 "f'{color7}  {tank7}{awards7}', inline=False)
        embed.add_field(name="9 "f'{color8}  {tank8}{awards8}', value="10"f'{color9}  {tank9}{awards9}', inline=False)
        
        await client.say(embed=embed)


@client.command()
async def pst(id):
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

@client.command(pass_context = True)
async def addprofile(ctx):
    userid = ctx.message.author.name
    sheet = Client.open("profile").sheet1
    cell_list = sheet.findall(f'{userid}')
    for userid in cell_list:
        await client.say("Profile already registerd use ``.mytanks`` to display your tanks")
        break
    else:
        data = sheet.get_all_records()
        row = [f"{userid}"]
        index = 2
        sheet.insert_row(row, index)
        await client.say("Follow Instructions in the DM")
        await client.send_message(ctx.message.author, '```You have been added to database```\nadd tanks with the following command``.tank1 "Example Tank" use tank2 to add second tank and so on``\nYou are able to do up to 6 tanks')

@client.command(pass_context = True)
async def tank1(ctx, link):
    userid = ctx.message.author.name
    sheet = Client.open("profile").sheet1
    cell = sheet.find(userid)
    row_number = cell.row
    sheet.update_cell(f'{row_number}', 2, f'{link}')
    await client.say('Tank has been added to database, Display tank in chat by using command ``.mytanks``')


@client.command(pass_context = True)
async def tank2(ctx, link):
    userid = ctx.message.author.name
    sheet = Client.open("profile").sheet1
    cell = sheet.find(userid)
    row_number = cell.row
    sheet.update_cell(f'{row_number}', 3, f'{link}')
    await client.say('Tank2 has been added to database')

    @client.command(pass_context = True)
    async def tank3(ctx, link):
        userid = ctx.message.author.name
        sheet = Client.open("profile").sheet1
        cell = sheet.find(userid)
        row_number = cell.row
        sheet.update_cell(f'{row_number}', 4, f'{link}')
        await client.say('Tank3 has been added to database')

    @client.command(pass_context = True)
    async def tank4(ctx, link):
        userid = ctx.message.author.name
        sheet = Client.open("profile").sheet1
        cell = sheet.find(userid)
        row_number = cell.row
        sheet.update_cell(f'{row_number}', 5, f'{link}')
        await client.say('Tank4 has been added to database')


    @client.command(pass_context = True)
    async def tank5(ctx, link):
        userid = ctx.message.author.name
        sheet = Client.open("profile").sheet1
        cell = sheet.find(userid)
        row_number = cell.row
        sheet.update_cell(f'{row_number}', 6, f'{link}')
        await client.say('Tank5 has been added to database')
        
@client.command(pass_context = True)
async def mytanks(ctx):
    userid = ctx.message.author.name
    embed = discord.Embed(title=f"Top Tanks of: {userid}", description="", color=0x00ff00)
    sheet = Client.open("profile").sheet1
    cell = sheet.find(userid)
    value = cell.value
    row_number = cell.row
    space ="\u200b"
    try:
        tank0 = sheet.row_values(f'{row_number}')[1]
    except IndexError:
        tank0=None
    if tank0 ==None:
        await client.say(f"{userid} has not added any tanks to profile")
    else:
        async with aiohttp.ClientSession()as session1:
            response1 = await session1.get(f'https://tankpit.com/api/find_tank?name={tank0}')
            await asyncio.sleep(1)
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=True)

    try:
        tank1 = sheet.row_values(f'{row_number}')[2]
    except IndexError:
        tank1=None
    if tank1 ==None:
        print("nothing")
    else:
        async with aiohttp.ClientSession()as session2:
            response2 = await session2.get(f'https://tankpit.com/api/find_tank?name={tank1}')
            await asyncio.sleep(1)
            resp_json2 = await response2.json()
            NAME2 = resp_json2[0]['name']
            awards2 = award_string(resp_json2[0]['awards'])
            embed.add_field(name=f'{NAME2}\n{awards2}', value=f"{space}", inline=True)
    try:
        tank2 = sheet.row_values(f'{row_number}')[3]
    except IndexError:
        tank2=None
    if tank2 ==None:
        print("nothing")
    else:
        async with aiohttp.ClientSession()as session3:
            response3 = await session3.get(f'https://tankpit.com/api/find_tank?name={tank2}')
            await asyncio.sleep(1)
            resp_json3 = await response3.json()
            NAME3 = resp_json3[0]['name']
            awards3 = award_string(resp_json3[0]['awards'])
            embed.add_field(name=f'{NAME3}\n{awards3}', value=f"{space}", inline=True)
    try:
        tank3=sheet.row_values(f'{row_number}')[4]
    except IndexError:
        tank3=None
    if tank3 ==None:
        print("nothing")

    else:
        async with aiohttp.ClientSession()as session4:
            response4 = await session4.get(f'https://tankpit.com/api/find_tank?name={tank3}')
            await asyncio.sleep(1)
            resp_json4 = await response4.json()
            NAME4 = resp_json4[0]['name']
            awards4 = award_string(resp_json4[0]['awards'])
            embed.add_field(name=f'{NAME4}\n{awards4}', value=f"{space}", inline=True)
    try:
        tank4=sheet.row_values(f'{row_number}')[5]
    except IndexError:
        tank4=None
    if tank4 ==None:
        print("nothing")
    else:
        async with aiohttp.ClientSession()as session5:
            response5 = await session5.get(f'https://tankpit.com/api/find_tank?name={tank4}')
            await asyncio.sleep(1)
            resp_json5 = await response5.json()
            NAME5 = resp_json5[0]['name']
            awards5 = award_string(resp_json5[0]['awards'])
            embed.add_field(name=f'{NAME5}\n{awards5}', value=f"{space}", inline=True)
    try:
        tank5=sheet.row_values(f'{row_number}')[6]
    except IndexError:
        tank5=None
    if tank5 ==None:
        print("nothing")
        await client.say(embed=embed)
    else:
        async with aiohttp.ClientSession()as session6:
            response6 = await session6.get(f'https://tankpit.com/api/find_tank?name={tank5}')
            await asyncio.sleep(1)
            resp_json6 = await response6.json()
            NAME6 = resp_json6[0]['name']
            awards6 = award_string(resp_json5[0]['awards'])
            embed.add_field(name=f'{NAME6}\n{awards6}', value=f"{space}", inline=True)

            await client.say(embed=embed)

#-----------events-------------------
@client.event#events = (function here) then function on the bottom to send out)
async def on_member_join(member):
    embed=discord.Embed(title="Welcome to the TankPit HQ Discord", description=" ",  color =0x7d2789)
    embed.set_thumbnail(url="https://tankpit.com/images/icons/orange_orb.png")
    embed.add_field(name="About", value="", inline=True)
    embed.add_field(name="Rules", value="", inline=True)
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
        role = discord.utils.get(message.server.roles, name='Active Units')
        await client.add_roles(message.author, role)
    if message.author == client.user:
        return
    if message.content == '.alertsoff':
        role = discord.utils.get(message.server.roles, name='Active Units')
        await client.remove_roles(message.author, role)
    if message.content.startswith('$hey'):
        await client.send_message(message.channel, 'Say hello')
        msg = await client.wait_for_message(author=message.author, content='hello')
        await client.send_message(message.channel, 'Hello.')
    await client.process_commands(message)

@client.command(name='alertson')
async def alerts_on():
    embed=discord.Embed(title="Tournament Alerts have been enabled 🔊", description="",  color =0x7d2789)
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
    server = member.server
    channel = discord.utils.get(member.server.channels, name="general")
    message = '{}'.format(member.mention)
    embed=discord.Embed(title=f" ", description=f"{message} has left the field",  color =0x7d2789)
    await client.send_message(channel, embed=embed)

#-----Bot Status-----------------------

@client.event
async def on_ready():
    embed = discord.Embed(title="", description="",  color =0xff0000)
    print("logged in as" + client.user.name)
    embed=discord.Embed(title="Tournament starting, prepare for battle! ", description="",  color =0x7d2789)
    channel = client.get_channel('476221292341886979')
    embed.set_footer(text='.alerts on to recieve notifcations .alertsoff to mute notifcations')
    while True:
        async with aiohttp.ClientSession()as sess1:
            channel = client.get_channel('476221292341886979')
            response = await sess1.get('https://tankpit.com/api/upcoming_tournaments')
            resp = await response.json()

            tourn = resp[0]['start_time_utc'][0:16] #TIME OF TOURNAMENT
            now = datetime.now() #TODAYS TIME (NOW)
            print(now)
            for f'{now}'[0:16] == tourn:
                try:
                    print("it worked lol")
                    await client.send_message(channel, '<@&468277182863769600>')
                    await client.send_message(channel, embed=embed)
                    await asyncio.sleep(60)
                except KeyError:
                    print(f'{now}'[0:16])
                    await client.send_message(channel, tourn)
                    await client.send_message(channel, embed=embed)
                    continue
            await asyncio.sleep(3)

       
#updatee

client.run(TOKEN)
