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


#'''---------------------------START-------------------------------'''
# SERVER_PREFIX=environ.get('BOT_PREFIX')
SERVER_PREFIX='-' 

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

    #create inv link
    inv_link = await channel.create_invite(max_age=0, max_uses=0, unique=False)
    
    try:
        #send private message
        await member.send(f'Welcome {member.mention},\n\n    Have a great time here in **{member.guild}**\n\n    Enjoyyyy:tada:\n\n    Here is the Invitation Link to this Server:\n    {inv_link}')
        with open('welcom_gifs.txt','r') as f:
            reader=f.readlines()
            gif_to_send=choice(reader)
        
        await member.send(gif_to_send)         #SEND GIFs
    except:
        pass


    try:
        channel = member.guild.get_channel(757225313943027772)
        await channel.edit(name=f'🧑｜𝗔𝗟𝗟-𝗠𝗘𝗠𝗕𝗘𝗥𝗦: {len(member.guild.members)}')
    except:
        memberr = await bot.fetch_user(483179796323631115)
        await memberr.send(f'Couldn\'n change the total member count')


    #-----------------------------------------------------------#WELCOME MESSAGE
    #GIVE MEMBER ROLE ON JOIN
    role_member = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role_member)


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
        await channel.edit(name=f'🧑｜𝗔𝗟𝗟-𝗠𝗘𝗠𝗕𝗘𝗥𝗦: {len(member.guild.members)}')
    except:
        memberr = await bot.fetch_user(483179796323631115)
        await memberr.send(f'Couldn\'n change the total member count')
    
    
    
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

                cmd= (i.content.strip().split('`',1)[1].split('`',1)[0]).strip()
                i=i.content

                if message.content.lower().strip()==cmd.lower().strip():

                    action=(i.split('`',1)[1].split('`',1)[1]).strip()
                    action=action.replace('[user]',f' {message.author.mention} ')
                    action=action[2:-2]
                    await message.channel.send(action)
                    await asyncio.sleep(1)
                    break
            except IndexError:
                await i.delete()

        
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
@bot.command(name='ClearMessages',  aliases=['clear','clearmsg','cls'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def clear(ctx, amount=0):
    """
    Delete Messages
    """

    if ctx.author.bot == False:
        if amount<100:
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.channel.purge(limit=100)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        pass
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
                await ctx.send(f':exclamation: The Command has already been added.')
            else:
                command_channel = bot.get_channel(757846893375258659)
                zero_bot_commands = bot.get_channel(757231675146108928)
                if len(args)>=2:
                    command_name=args[0].strip()
                    if command_name[0]==SERVER_PREFIX:
                        await ctx.send(f':exclamation: Please do not use Server Prefix as a Custom Command Prefix')
                    else:
                        action=(' '.join(args[1:])).strip()
                        spaces= ' '*(18-(len(command_name)))
                        await zero_bot_commands.send(f'` {command_name} `{spaces}   **{action}**')
                        await command_channel.send(f'{command_name}{" "*5}{action}{" "*5}**AddedBy:** {ctx.message.author.mention}  **On:** `{datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S")}`.')
                        
                        await ctx.message.add_reaction('☑')
        except IndexError:
            await ctx.send(f':exclamation: The CORRECT Format for Adding a Command is:\n**```  {SERVER_PREFIX}addcom [command-name] [action]  ```**')

@addcom.error
async def addcom_error(ctx, error):
    if isinstance(error, commands.errors.MissingAnyRole):
        pass
    elif isinstance(error, commands.errors):
        await ctx.send(f':exclamation: The CORRECT Format for Adding a Command is:\n**```  {SERVER_PREFIX}addcom [command-name] [action]  ```**')
 #========================================================  
#Delete COmmand command


@bot.command(name='DeleteCustomCommand', aliases=['delcom','deletecommand'])
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
                    await ctx.message.add_reaction('☑')
                    
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
                await ctx.send(f'{ctx.message.author.mention}\n:x: Command not Found')


        except IndexError:
            await ctx.send(f':exclamation: The CORRECT Format for deleting a Command is:\n**```  {SERVER_PREFIX}delcom [command-name] ```**')


@delcom.error
async def delcom_error(ctx, error):
    if isinstance(error, commands.errors.MissingAnyRole):
        pass
    elif isinstance(error, commands.errors):
        await ctx.send(f':exclamation: The CORRECT Format for deleting a Command is:\n**```  {SERVER_PREFIX}delcom [command-name] ```**')

#========================================================  
#USER INFO



@bot.command(name="UserInformation", aliases=["userinfo", "ui"])
async def user_info(ctx, target: Optional[Member]):
    """
    All the Information about the User
    """

    if ctx.author.bot == False:
        target = target or ctx.author

        embed = Embed(title="User Information",
                        colour=target.colour)

        embed.set_thumbnail(url=target.avatar_url)

        fields = [                    
                    ("Name", f'{str(target)} {"**Bot**" if target.bot else ""}', True),
                    ('Nickname', str(target.nick),True),
                    ("Top role", target.top_role.mention, True),

                    ("Status", str(target.status).title(), True),
                    ("Activity", f"*{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'}* **{target.activity.name if target.activity else ''}**", True),
                    ("Joined at", target.joined_at.strftime("%b %d, %Y "), False)
                    

                    # ("Created at", target.created_at.strftime("%b %d, %Y "), True),
                    # ("Boosted", bool(target.premium_since), True)
                    # # ("ID", target.id, True)

                ]
                    
                

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
 #========================================================   
#SERVER INFO



@bot.command(name="ServerInformation", aliases=['serverinfo', 'si'])
async def server_info(ctx):
    """
    All the Information about the server.
    """
    if ctx.author.bot == False:
        embed = Embed(title="Server Information",
                        colour=ctx.guild.owner.colour)

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields =[
                    
                    
                    ("Owner", f'{ctx.guild.owner.mention}', True),
                    ("Region", f'{str(ctx.guild.region).title()}', True),
                    ("Created on", ctx.guild.created_at.strftime("%b %d, %Y "), True),
                    
                    ("Members", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                    ("Roles", len(ctx.guild.roles), True),
                    ("Banned", len(await ctx.guild.bans()), True),

                    ("Emojis", len(ctx.guild.emojis), True),
                    ("Text channels", len(ctx.guild.text_channels), True),
                    ("Voice channels", len(ctx.guild.voice_channels), True),
                    

                    ("\u200b",f"**🟢 {statuses[0]}｜🟠 {statuses[1]}｜🔴 {statuses[2]}｜⚪ {statuses[3]}**", False),
                    

                    # ("ID", f'{ctx.guild.id}', True),
                    # ("Members", len(ctx.guild.members), True),
                    # ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                    # ("Invites", len(await ctx.guild.invites()), True),
                    
                ]

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
            
            try:
                count=args[0][1]
                for i in range(int(count)):
                    send=' '.join(list(args)[1:])
                    await ctx.send(send)
                    await asyncio.sleep(0.5)
            except:
                send=' '.join(list(args))
                await ctx.send(send)
        else:
            send=' '.join(list(args))
            await ctx.send(send)
 #========================================================

#FORMAT COMMANDS
@bot.command(name='FormatCommand', aliases=['forcom','formatcommands'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def formatcommands(ctx):
    """
    Format The Zero-bot-Commands Channel.
    """
    if ctx.author.bot == False:

        zero_bot_channel = bot.get_channel(757231675146108928)
        messages_ = await zero_bot_channel.history(limit=1000).flatten()

        all_messages=[]
        for i in messages_:
            if not i.id ==(758232573205020693):
                all_messages.append(i.content)

        
        all_messages.reverse()

        await zero_bot_channel.purge(limit=len(all_messages))


        for i in all_messages:
            await zero_bot_channel.send(i)
            await asyncio.sleep(1)
        await ctx.message.add_reaction('☑')
        


@bot.command(name='LogOutBot', aliases=['logout','close'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def LogOut(ctx):
    """
    Closes The Bot
    """
    if ctx.author.bot == False:
        memberr = await bot.fetch_user(483179796323631115)
        
        await ctx.message.add_reaction('☑')
        await memberr.send(f'Logged Out by: **{ctx.author.id}** || on `{datetime.utcnow().strftime(datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S"))}`')
        await ctx.send(f'Bye Bye')
        await bot.close()


#CHoose between objects
@bot.command(name='Choice', aliases=['choose','chs'])
async def choise(ctx, *args):
    """
    Choose between different items.
    """

    await ctx.send(f'> {choice(args)}')

#Roll Random Numbers
@bot.command(name='RollNumber', aliases=['roll','rnd'])
async def roll(ctx,a=0,b=100):
    """
    Roll a random number between the specified interval.(Deafult 0-100)
    """
    try:
        a=int(a)
        b=int(b)

        if a>b:
            a,b= b,a
        nums=[i for i in range(a,b+1,1)]

        await ctx.send(f'> {choice(nums)}')
    except:
        pass

@bot.command(name="Invitaion",aliases=['cinv','invitationlink'])
async def inv(ctx):
    """
    Create a Invitaion Link for the Server.
    """
    inv_link = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=False)
    await ctx.send(inv_link)
    


#print Zer0
@bot.command(name='Zer00', aliases=['zer0'])
async def zer0(ctx):
    """
    Zeroooooooooo0000000000
    """
    a='''
		         ,----,                                    
		       .'   .`|                  ,----..           
		    .'   .'   ;                 /   /   \          
		  ,---, '    .'        __  ,-. /   .     :         
		  |   :     ./       ,' ,'/ /|.   /   ;.  \        
		  ;   | .'  /  ,---. '  | |' .   ;   /  ` ;        
		  `---' /  ;  /     \|  |   ,;   |  ; \ ; |        
		    /  ;  /  /    /  '  :  / |   :  | ; | '        
		   ;  /  /--.    ' / |  | '  .   |  ' ' ' :        
		  /  /  / .`'   ;   /;  : |  '   ;  \; /  |        
		./__;       '   |  / |  , ;   \   \  ',  /         
		|   :     .'|   :    |---'     ;   :    /          
		;   |  .'    \   \  /           \   \ .'           
		`---'         `----'             `---`           
                                                   
        '''

    await ctx.send(f'```{a}```')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        pass
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        pass


DISCORD_TOKEN = environ.get('DISCORD_TOKEN') 

# bot.run(DISCORD_TOKEN)
bot.run('NzU2ODE2NTEzMDM3NzYyNTgx.X2XWTQ.h-3pujN5KbKbqnDsAhtVq7RRHKQ')




    
#JSON JOINN AND LEAVE  
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
            json.dump(data,g, indent=4)   
    
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
            json.dump(data,g, indent=4)
            '''

    #'Member': 756428207200403477,
    # 'OP': 756534460173779044,
    # '🛡️│Bots': 756429809759813683,
    # 'GUYZ': 756487678668701747,
    # 'MOD': 756410200172396595,
    # 'ADMIN': 756398801874321408,
    # '乙乇尺回': 756435470623309836