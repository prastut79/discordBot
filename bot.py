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

import asyncio

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
SERVER_PREFIX=environ.get('BOT_PREFIX')
# SERVER_PREFIX='-'

bot = commands.Bot(command_prefix=SERVER_PREFIX, case_insensitive=True)



#bot Start
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="ANIMEEE"))
    print('Bot is Online. GTG')
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
bot.remove_command('delcom')

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
#ON MESSAGE

@bot.event
async def on_message(message):
    if message.author.bot==False:
        #channel where the commands are stored   
        channel = bot.get_channel(757231675146108928)
        #getting all messages from the channel
        commands_ = await channel.history(limit=1000).flatten()

        for i in commands_:
            try:
                cmd= ((i.content.strip().split('`',1)[1].split('`',1)[0]))
                i=i.content.strip()
                if str(message.content).lower().strip()==cmd.lower().strip():

                    action=(i.split('`',1)[1].split('`',1)[1]).strip()
                    action=action.replace('[user]',f' {message.author.mention} ')
                    await message.channel.send(action[2:-2])
                    break
            except IndexError:
                await i.delete()

        await asyncio.sleep(5)
        
        await bot.process_commands(message)




#========================================================
#Ping Command
@bot.command(name='BotPing', aliases=['ping'])
async def _bot_ping(ctx):
    """
    Ping the Bot
    """

    if ctx.author.bot == False:
        await ctx.send(f'Ping: {int(round(bot.latency*1000,1))}ms')
#========================================================
 


#Clear Message Command
@bot.command(name='ClearMessages',  aliases=['clear','clearmsg'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def clear(ctx, amount=0):
    """
    Delete Messages
    """
    if ctx.author.bot == False:
        await ctx.channel.purge(limit=amount+1)
    # await ctx.send(f'Deleted {amount} messages')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Sorry you are not allowed to use this command.')
 #========================================================   
#add COmmand command



@bot.command(name='AddCommand', aliases=['addcom'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')

#checking if the commands is added or not
async def addcom(ctx, *args):
    """
    Add a Command
    """

    if ctx.author.bot == False:

        try:
            dublicate_command= False
            channel = bot.get_channel(757231675146108928)               #channel where the commands are stored   
            commands_ = await channel.history(limit=1000).flatten()         #getting all messages from the channel
            for i in commands_:
                cmd= (i.content.strip().split('`',1)[1].split('`',1)[0]).strip()
                command_name=args[0].strip()
                if cmd.lower() == command_name.lower():
                    dublicate_command=True
                    break


            #adding command only if it already hasnt been added
            if dublicate_command:
                await ctx.send(f'{ctx.message.author.mention}\nThe Command has already been added.')
            else:
                command_channel = bot.get_channel(757846893375258659)
                zero_bot_commands = bot.get_channel(757231675146108928)
                # if len(args)>=2:
                command_name=args[0].strip()
                if command_name[0]==SERVER_PREFIX:
                    await ctx.send(f'{ctx.message.author.mention}\nPlease donot use Server Prefix as a Custom Command Prefix')
                else:
                    action=(' '.join(args[1:])).strip()
                    spaces= ' '*(18-(len(command_name)))
                    await zero_bot_commands.send(f'` {command_name} `{spaces}   **{action}**')
                    await command_channel.send(f'{command_name}{" "*5}{action}{" "*5}**AddedBy:** {ctx.message.author.mention}  **On:** `{datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S")}`.')
                    
                    await ctx.send(f'{ctx.message.author.mention}\nThe Command ` {command_name} ` was added.')
        except IndexError:
            await ctx.send(f'{ctx.message.author.mention}\nThe Command wasn\'t added.\nThe CORRECT Format for Adding a Command is:\n**```  {SERVER_PREFIX}addcom [command-name] [action]  ```**')

@addcom.error
async def addcom_error(ctx, error):
    if isinstance(error, commands.errors.MissingAnyRole):
        await ctx.send(f'{ctx.message.author.mention}, you are not allowed to use this Command.')
    elif isinstance(error, commands.errors):
        await ctx.send(f'{ctx.message.author.mention}\nThe Command wasn\'t added.\nThe CORRECT Format for Adding a Command is:\n**```  {SERVER_PREFIX}addcom [command-name] [action]  ```**')
 #========================================================  
#Delete COmmand command


@bot.command(name='DeleteCommand', aliases=['delcom'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')

async def delcom(ctx,*, command):
    """
    Delete a Command
    """

    if ctx.author.bot == False:

        try:
            #checking if the commands exists or not
            command_found=False
            channel = bot.get_channel(757846893375258659)               #channel where the commands are stored   
            commands_ = await channel.history(limit=1000).flatten()         #getting all messages from the channel
            for i in commands_:
                cmd=(i.content).split(' ')[0]
                if command.lower() == cmd.lower():
                    command_found=True
                    await i.delete()
                    await ctx.send(f'{ctx.message.author.mention}\nThe command `{command}` has been deleted.')

                    #channel where deleted commands are stored
                    channel = bot.get_channel(757955355736014848)    
                    await channel.send(f'{i.content} **DeletedBy:** {ctx.message.author.mention}  **On:** `{datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S")}`.')
                    break
            
            #DELETING FROM Zero-bot-commands  CHANEL AS WELL
            if command_found:
                channel = bot.get_channel(757231675146108928)              
                commands_ = await channel.history(limit=1000).flatten()   

                for i in commands_:
                    cmd=((i.content).replace('`','')).strip()
                    cmd=cmd.split(' ')[0]
                
                    if str(command).lower()==cmd.lower():
                        await i.delete()
                        break

            else:
                await ctx.send(f'{ctx.message.author.mention}\nCommand not Found')


        except IndexError:
            await ctx.send(f'{ctx.message.author.mention}\nThe Command wasn\'t delete.\nThe CORRECT Format for deleting a Command is:\n**```  {SERVER_PREFIX}delcom [command-name] ```**')

    

    
@delcom.error
async def delcom_error(ctx, error):
    if isinstance(error, commands.errors.MissingAnyRole):
        await ctx.send(f'{ctx.message.author.mention}, you are not allowed to delete Commands.')
    elif isinstance(error, commands.errors):
        await ctx.send(f'{ctx.message.author.mention}\nThe Command wasn\'t delete.\nThe CORRECT Format for deleting a Command is:\n**```  {SERVER_PREFIX}delcom [command-name] ```**')
 #========================================================  
#USER INFO



@bot.command(name="UserInformation", aliases=["memberinfo", "ui",'uinfo', "info"])
async def user_info(ctx, target: Optional[Member]):
    """
    All the Information about the User
    """

    if ctx.author.bot == False:
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
 #========================================================   
#SERVER INFO



@bot.command(name="ServerInf0rmation", aliases=['serverinformation','serverinfo','sinfo', "si"])
async def server_info(ctx):
    """
    All the Information about the server.
    """
    if ctx.author.bot == False:
        embed = Embed(title="Server Information",
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

@bot.command(name='RepeatUser', aliases=['say','repeat'])
async def say(ctx, *args):
    """
    Repeat The User.
    """
    
    if ctx.author.bot == False:
        if args[0][0] == (f'{SERVER_PREFIX}'):
            count=args[0][-1]
            try:
                for i in range(int(count)):
                    send=' '.join(list(args)[1:])
                    await ctx.send(send)
            except:
                send=' '.join(list(args))
                await ctx.send(send)
        else:
            send=' '.join(list(args))
            await ctx.send(send)
 #========================================================   

#FORMAT COMMANDS
@bot.command(name='FormatCommand', aliases=['forcom','fcom','formatcom', 'formatcommands'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def formatcommands(ctx):
    """
    Format The Zero-bot-Commands Channel.
    """
    if ctx.author.bot == False:

        zero_bot_channel = bot.get_channel(757231675146108928)
        messages_ = await zero_bot_channel.history(limit=1000).flatten()
        
        all_messages=[i.content for i in messages_]
        all_messages.reverse()

        await zero_bot_channel.purge(limit=len(messages_))


        for i in all_messages:
            await zero_bot_channel.send(i)
            await asyncio.sleep(1.2)
        await ctx.send(f'{ctx.author.mention}\nAll Comments Updated')


@bot.command(name='LogOutBot', aliases=['logout','close'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def LogOut(ctx):
    """
    Closes The Bot
    """
    if ctx.author.bot == False:
        memberr = await bot.fetch_user(483179796323631115)
        

        await memberr.send(f'Logged Out by: **{ctx.author.id}** || on `{datetime.utcnow().strftime(datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S"))}`')
        await ctx.send(f'Bye Bye')
        await bot.close()







DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
bot.run(DISCORD_TOKEN)




    
  
