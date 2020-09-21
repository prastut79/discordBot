#https://discordpy.readthedocs.io/en/latest/logging.html
#https://github.com/netsos798/pybot/blob/master/bot.py
#https://dashboard.heroku.com/apps/py-bot-discord-798/logs
#git add . , git commit -m "das", git push

from os import environ
from datetime import datetime 
from typing import Optional
import csv


import discord
from discord.ext import commands
from random import choice 
from discord import Embed, Member
from discord.ext.commands import command
from discord.ext import tasks


HEX_COLORS=[
    0x4B4CAD, 0xA2D7CC, 0x74AD4B, 0x000000, 0x52fff1, 0xFF51EB, 0xC481A7, 0xffadad, 0xe29578, 0xBD93BD,
    0x22223b, 0x9DBBAE, 0x188FA7, 0x8C5F66, 0xADBCA5, 0xE8B9AB, 0xCB769E, 0x72B01D, 0xF7717D, 0x925E78,
    0x7F2982, 0x16001E, 0x610345, 0x044B7F, 0xF05365, 0xA1CDF1, 0xC3A197, 0xDBE4EE, 0xdeaaff, 0x00296b
]

ANIME_GIRL_GIFS=[
    'https://tenor.com/view/welcome-anime-smile-pretty-cute-gif-16579247',
    'https://tenor.com/view/anime-love-smiling-menhera-hearts-gif-12479110',
    'https://media1.tenor.com/images/528bb500b7d0cba55047ef0122e7f093/tenor.gif?itemid=14298094',
    'https://tenor.com/view/anime-welcome-home-master-gif-7922606',
    'https://tenor.com/view/welcome-home-anime-wave-smile-welcome-gif-15859070',
    'https://tenor.com/view/welcome-anime-mask-greetings-gif-17495343',
    'https://tenor.com/view/anime-animu-welcome-gif-15151790',
    'https://tenor.com/view/anime-animegirl-happy-gif-8273080',
    'https://tenor.com/view/anime-bed-sleep-animegirl-coffee-tea-relax-anime-anime-girl-gif-13116453',
    'https://tenor.com/view/anime-girl-girls-animegirl-red-gif-5578936',
    'https://tenor.com/view/anime-welcome-gif-4505891',
    'https://media.tenor.com/images/0916a65deb648ea999661c349441c8d2/tenor.gif',
    'https://media.tenor.com/images/07ef31853915cbdd38577d7ea82936de/tenor.gif',
    'https://tenor.com/view/anime-girl-keijo-anime-girl-kiss-gif-16974725',
    'https://tenor.com/view/gochiusa-welcome-anime-cute-gif-15822198',
    'https://tenor.com/view/anime-girl-gif-18150239',
    'https://tenor.com/view/anime-animegirl-happy-gif-8273080'
]

#'''---------------------------START-------------------------------'''

bot = commands.Bot(command_prefix=environ.get('BOT_PREFIX'), case_insensitive=True)
#
#bot Start
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="ANIMEEE"))
    print('Bot is ready')
    # # Setting `Playing ` status
    # await bot.change_presence(activity=discord.Game(name="a game"))
    # # Setting `Streaming ` status
    # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
    # # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
    # # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
#========================================================


#Serve Join
@bot.event#member.id
async def on_member_join(member):
    #WELCOME MESSAGE------------------------------------------------------------
    embed=discord.Embed(color=choice(HEX_COLORS), 
        description=f'\n\n{member.mention}, Welcome to **{member.guild}**.:tada:\n\nMember **#{len(list(member.guild.members))}**'
        )
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'\n{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp = datetime.utcnow()

    channel = member.guild.get_channel(756417893314461766)

    await channel.send(embed=embed)


    #send private message
    await member.send(f'\nWelcome {member.mention},\n\n    You have been assigned the role of **`Member`** and **`DJ`**.\n\n    Have a great time here in **{member.guild}**\n\n    Enjoy:tada:\n\n    Also, Invite your friends to this server:\n    https://discord.gg/X64nvv6')
    await member.send(choice(ANIME_GIRL_GIFS))         #SEND GIFs




    channel = member.guild.get_channel(757225313943027772)
    await channel.edit(name=f'All Members: {len(member.guild.members)}')


    #-----------------------------------------------------------#WELCOME MESSAGE
    #GIVE DJ AND MEMBER ROLE ON JOIN
    role_member = discord.utils.get(member.guild.roles, name='Member')
    role_dj = discord.utils.get(member.guild.roles, name='DJ')
    await member.add_roles(role_member, role_dj)

'''
     #OPENING JSON FILE
    with open('discord_member_info.json','r') as f:
        data=json.load(f)

    if str(member.guild)=='Netsos':
        #when joining
        new_user=True
        for i in data['members_info']:
            if i['user_id']==member.id:
                i['name'].append(member.name+'#'+member.discriminator)
                i["member_count"].append(len(list(member.guild.members)))
                i['joined_status']=True
                i['joined_date'].append(str(datetime.utcnow())+' UTC')
                i['join_count']+=1
                i["nicknames"].append(member.nick)
                i['leave_status']=False

                new_user=False
                break
            

        if new_user:
            dic={
                    "user_id": member.id,
                    "name": [member.name+'#'+member.discriminator],
                    "member_count": [len(list(member.guild.members))],
                    "joined_status": True,
                    "joined_date": [str(datetime.utcnow())+' UTC'],
                    "join_count": 1,
                    "leave_status": False,
                    "leave_date": [],
                    "leave_count": 0,
                    "roles": [],
                    "nicknames": [member.nick]
                }
            data['members_info'].append(dic)

        
        #WRITING TO JSON FILE
        with open('discord_member_info.json','w') as g:
            json.dump(data,g, indent=4)'''
#========================================================



#Server Leave
@bot.event
async def on_member_remove(member):
    embed=discord.Embed(color=choice(HEX_COLORS), description=f'**{member.name}** has left the server.\nGoodBye:wave:')
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp = datetime.utcnow()

    channel = member.guild.get_channel(756452827395784775)

    await channel.send(embed=embed)



    #TOTAL MEMBERS COUNT
    try:
        channel = member.guild.get_channel(757225313943027772)
        await channel.edit(name=f'All Members: {len(member.guild.members)}')
    except:
        pass
'''
    if str(member.guild)=='Netsos':
        #OPENING JSON FILE
        with open('discord_member_info.json','r') as f:
            data=json.load(f)

        #when leaving
        for i in data['members_info']:
            if i['user_id']==member.id:
                i['leave_status']=True
                i['leave_date'].append(str(datetime.utcnow())+' UTC')
                i['leave_status']=True
                i['leave_count']+=1
                break

        #WRITING TO JSON FILE
        with open('discord_member_info.json','w') as g:
            json.dump(data,g, indent=4)   '''
#========================================================


@bot.event
async def on_message(message):
    
    if not message.author.bot == True:
        with open('commands.csv','r') as f:
            reader=csv.DictReader(f)
            for line in reader:
                if line['command'] in str(message.content).lower():
                    await message.channel.send (f"{message.author.mention} {line['task']} ")
                    break
    await bot.process_commands(message)
    


#========================================================
#Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping: {int(round(bot.latency*1000,1))}ms')
#========================================================
 


#Clear Message Command
@bot.command()
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def clear(ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        # await ctx.send(f'Deleted {amount} messages')
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Sorry you are not allowed to use this command.')
 #========================================================   


#USER INFO

@bot.command(name="uSeRiNfO", aliases=["memberinfo", "ui",'uinfo', "info"])
async def user_info(ctx, target: Optional[Member]):
    target = target or ctx.author

    embed = Embed(title="User Information",
                    colour=target.colour,
                    timestamp=datetime.utcnow())

    embed.set_thumbnail(url=target.avatar_url)

    fields = [("Name", str(target), True),
                ("ID", target.id, True),
                ("Bot?", target.bot, True),
                ("Top role", target.top_role.mention, True),
                ("Status", str(target.status).title(), True),
                ("Activity", f"*{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'}* **{target.activity.name if target.activity else ''}**", True),
                ("Created at", target.created_at.strftime("%b %d, %Y "), True),
                ("Joined at", target.joined_at.strftime("%b %d, %Y "), True)]
                # ("Boosted", bool(target.premium_since), True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)
 #========================================================   \


#SERVER INFO

@bot.command(name="sErVeRiNf0", aliases=['serverinformation','sinfo', "si"])
async def server_info(ctx):
    embed = Embed(title="Server information",
                    colour=ctx.guild.owner.colour,
                    timestamp=datetime.utcnow())

    embed.set_thumbnail(url=ctx.guild.icon_url)

    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

    fields = [("ID", ctx.guild.id, True),
                ("Owner", ctx.guild.owner, True),
                ("Region", str(ctx.guild.region).title(), True),
                ("Created on", ctx.guild.created_at.strftime("%b %d, %Y %H:%M:%S"), True),
                ("Members", len(ctx.guild.members), True),
                ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                ("Banned members", len(await ctx.guild.bans()), True),
                ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                ("Text channels", len(ctx.guild.text_channels), True),
                ("Voice channels", len(ctx.guild.voice_channels), True),
                ("Categories", len(ctx.guild.categories), True),
                ("Roles", len(ctx.guild.roles), True),
                ("Invites", len(await ctx.guild.invites()), True),
                ("\u200b", "\u200b", True)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)
 #========================================================   







bot.run(environ.get('DISCORD_TOKEN'))
# bot.run('NzU2ODE2NTEzMDM3NzYyNTgx.X2XWTQ.h-3pujN5KbKbqnDsAhtVq7RRHKQ')


    
  
