#https://discordpy.readthedocs.io/en/latest/logging.html
#whitespace = \u200b 

from os import environ
from datetime import datetime 
from typing import Optional
import csv
import random
from time import time
import smtplib
import json

import discord
from discord.ext import commands
from discord import Embed, Member
from discord.ext.commands import command, cooldown , BucketType                 

import asyncio

BOT_OWNER_ID = 483179796323631115
BOT_ID = 756816513037762581

HEX_COLORS=[
    0x4B4CAD, 0xA2D7CC, 0x74AD4B, 0x000000, 0x52fff1, 0xFF51EB, 0xC481A7, 0xffadad, 0xe29578, 0xBD93BD,
    0x22223b, 0x9DBBAE, 0x188FA7, 0x8C5F66, 0xADBCA5, 0xE8B9AB, 0xCB769E, 0x72B01D, 0xF7717D, 0x925E78,
    0x7F2982, 0x16001E, 0x610345, 0x044B7F, 0xF05365, 0xA1CDF1, 0xC3A197, 0xDBE4EE, 0xdeaaff, 0x00296b,
    0x000000, 0xffffff
]


#'''---------------------------START--------------------------------'''
with open('server_config.json','r') as f:
    SERVER_CONFIG = json.load(f)
# print(type(SERVER_CONFIG['welcome_message_channel']))

bot = commands.Bot(command_prefix=SERVER_CONFIG['server_prefix'], case_insensitive=True)
# bot.remove_command('help')



#bot Start
@bot.event
async def on_ready():
    await bot.change_presence(
            status=discord.Status.idle, 
            activity=discord.Activity(type=discord.ActivityType.watching, name="ANIMEEE")
    )
    print('Bot is Online. GTG')
    with open('time.txt','w') as f:
        time=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        f.write(time)


@bot.command()
async def uptime(ctx):
    if ctx.author.id == BOT_OWNER_ID:
        with open('time.txt','r') as f:
            a=f.readline()
            online_time= datetime.strptime(a, "%m/%d/%Y, %H:%M:%S")
            c_time=datetime.now()
            uptime= str(c_time - online_time).split('.')[0] 

        embed=Embed(
            color=random.choice(HEX_COLORS),
            description=f'⌛ **UpTime:** {uptime}'
        )
        await ctx.send(embed=embed)

@bot.command()
async def aplaying(ctx,*name):
    if ctx.author.id == BOT_OWNER_ID:
        name=' '.join(list(name))
        await bot.change_presence(
                status=discord.Status.idle, 
                activity= discord.Game(name= name)
        )
        await ctx.message.add_reaction('☑')

@bot.command()
async def astreaming(ctx, url, *name):
    if ctx.author.id == BOT_OWNER_ID:
        name = ' '.join(list(name))
        await bot.change_presence(
                status=discord.Status.idle,
                activity=discord.Streaming(name= name,  url=url)
        )
        await ctx.message.add_reaction('☑')

@bot.command()
async def awatching(ctx,*name):
    if ctx.author.id == BOT_OWNER_ID:
        name= ' '.join(list(name))
        await bot.change_presence(  
                status=discord.Status.idle, 
                activity=discord.Activity(type=discord.ActivityType.watching, name=name)
        )
        await ctx.message.add_reaction('☑')

@bot.command()
async def alistening(ctx,*name):
    if ctx.author.id == BOT_OWNER_ID:
        name=' '.join(list(name))
        await bot.change_presence(
                status=discord.Status.idle, 
                activity=discord.Activity(type=discord.ActivityType.listening, name=name)
        )
        await ctx.message.add_reaction('☑')

#Ping Command
@bot.command(name='BotPing', aliases=['ping'])
@commands.cooldown(1, 5, BucketType.guild)
async def _bot_ping(ctx):
    """
    Ping the Bot
    """
    if ctx.author.bot == False:
        start= time()
        message = await ctx.send('**Pinging...**')
        end= time()

        description=f'⌛ **Latency:** {int(round(bot.latency*1000,1))}ms \n\u200b\n⏰ **Response Time:** {int((end-start)*1000)}ms'

        embed= discord.Embed(
                color=random.choice(HEX_COLORS), 
                description=description
            )

        await message.edit(content='',embed=embed)

@_bot_ping.error
async def ping_error(ctx, error):
    if not isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send( f'**There was an error while Pinging the bot.**')


#========================================================


#Serve Join
@bot.event#member.id
async def on_member_join(member):
    #WELCOME MESSAGE------------------------------------------------------------
    embed=Embed(color=random.choice(HEX_COLORS), 
                        description=f'{member.mention}, Welcome to **{member.guild}**.:tada:\n\nMember **#{len(list(member.guild.members))}**'
        )
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp = datetime.utcnow()
    

    #send welcome message
    welcome_message_channel = member.guild.get_channel(SERVER_CONFIG['welcome_message_channel'])
    welcome_msg= await welcome_message_channel.send(embed=embed)
    
    #add reaction
    welcome_emoji = discord.utils.get(member.guild.emojis, name='welcome')
    await welcome_msg.add_reaction(welcome_emoji)

    #EDIT TOTAL MEMBER COUNT
    member_count_channel = member.guild.get_channel(SERVER_CONFIG['member_count_channel'])
    await member_count_channel.edit(name=f'🧑｜MEMBERS: {len(member.guild.members)}')

    #GIVE ROLE ON JOIN
    role_to_give_on_join = list(SERVER_CONFIG['role_to_give_on_join'])
    for i in role_to_give_on_join:
        role_to_give_on_join = discord.utils.get(member.guild.roles, id=i)
        await member.add_roles(role_to_give_on_join)
        asyncio.sleep(1)

    #_--------------------SEND DM---------------------------------------------
    #create inv link
    inv_link = await welcome_message_channel.create_invite(max_age=0, max_uses=0, unique=False)

    welcome_dm = f'''\
Welcome {member.mention}

Have a great time here in **{member.guild}**

Enjoyyyy:tada:
    
Here is the Invitation Link to this Server:
{inv_link}
    '''
    #gifs
    with open('welcome_gifs.txt','r') as f:
        gifs = f.readlines()
        
    embed= Embed(
        color= random.choice(HEX_COLORS),
        description=welcome_dm
        )
    embed.set_image(url=random.choice(gifs))
    await member.send(embed=embed)

#========================================================


#Server Leave
@bot.event
async def on_member_remove(member):
    embed=Embed(
            color=random.choice(HEX_COLORS), 
            description=f'**{member.name}** has left the server.\nGoodBye:wave:'
        )
    embed.set_thumbnail(url=f'{member.avatar_url}')
    embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
    embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    embed.timestamp = datetime.utcnow()

    #SEND GOODBYE MESSAGE
    goodybye_channel = member.guild.get_channel(SERVER_CONFIG['goodbye_message_channel'])
    await goodybye_channel.send(embed=embed)

    #EDIT TOTAL MEMBER COUNT
    member_count_channel = member.guild.get_channel(SERVER_CONFIG['member_count_channel'])
    await member_count_channel.edit(name=f'🧑｜MEMBERS: {len(member.guild.members)}')

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


 #DM MESSAGE
@bot.command()
async def dm(ctx, user:discord.Member, *message): 
    if ctx.author.id == BOT_OWNER_ID:
        message= ' '.join(list(message))
        await user.send(message)
        await ctx.message.add_reaction('☑')

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(f'{ctx.author.mention}\nMember not Found.')
 
 #========================================================   


#Clear Message Command
@bot.command(name='ClearMessages',  aliases=['clear','clearmsg','cls'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')

async def clear(ctx, amount=1):
    """
    Delete Messages
    """

    if ctx.author.bot == False:
        if amount<100:
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.channel.purge(limit=100)

 
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
                        await ctx.send(f':exclamation: Please do not use Server Prefix as a Custom Command Prefix.')
                    else:
                        action=(' '.join(args[1:])).strip()
                        spaces= ' '*(18-(len(command_name)))
                        await zero_bot_commands.send(f'` {command_name} `{spaces}   **{action}**')
                        await command_channel.send(f'{command_name}{" "*5}{action}{" "*5}**AddedBy:** {ctx.message.author.mention}  **On:** `{datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S")}`.')
                        
                        await ctx.message.add_reaction('☑')
        except IndexError:
            await ctx.send(f':exclamation: The CORRECT Format for Adding a Command is:\n**```  {SERVER_PREFIX}addcom [command-name] [action]  ```**')

 #========================================================  


#Delete COmmand command
@bot.command(name='DeleteCustomCommand', aliases=['delcom','deletecommand'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
# @commands.cooldown(1,60*60*24,BucketType.member)
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
                await ctx.send(f'{ctx.message.author.mention}\n:x: Command not Found.')


        except IndexError:
            await ctx.send(f':exclamation: The CORRECT Format for deleting a Command is:\n**```  {SERVER_PREFIX}delcom [command-name] ```**')


#========================================================


#USER INFO
@bot.command(name="UserInformation", aliases=["userinfo", "ui"])
# @commands.cooldown(2,60*60,BucketType.member)
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
@commands.cooldown(5,60*60*24,BucketType.guild)
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
                    

                    ("\u200b",f"**🟢  {statuses[0]}｜🟠  {statuses[1]}｜🔴  {statuses[2]}｜⚪  {statuses[3]}**", False),
                    

                    # ("ID", f'{ctx.guild.id}', True),
                    # ("Members", len(ctx.guild.members), True),
                    # ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                    # ("Invites", len(await ctx.guild.invites()), True),
                ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
 
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
        
 
 #========================================================  


@bot.command(name='RepeatUser', aliases=['say','repeat'])
# @commands.cooldown(1,60,BucketType.member)
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


#CHoose between objects
@bot.command(name='Choice', aliases=['choose','chs'])
# @commands.cooldown(1,60,BucketType.member)
async def choise(ctx, *args):
    """
    Choose between different items.
    """

    await ctx.send(f'> {random.choice(args)}')
 
 #========================================================  


#Roll Random Numbers
@bot.command(name='RollNumber', aliases=['roll','rnd'])
# @commands.cooldown(1,60,BucketType.member)
async def roll(ctx,a,b=0):
    """
    Roll a random number between the specified interval.(Deafult 0-100)
    """
    try:
        a=int(a)
        b=int(b)

        if a>b:
            a,b= b,a
        nums=[i for i in range(a,b+1,1)]

        await ctx.send(f'> {random.choice(nums)}')
    except:
        pass
 
 #========================================================  


#create inv link
@bot.command(name="Invitaion",aliases=['cinv','invitationlink'])
@commands.cooldown(1,60*10,BucketType.member)
async def inv(ctx):
    """
    Create a Invitaion Link for the Server.
    """
    channel = ctx.guild.get_channel(756417893314461766)
    inv_link = await channel.create_invite(max_age=0, max_uses=0, unique=False)

    await ctx.author.send(f'Here is the Invitation link to This server\n{inv_link}')
 
 #========================================================      

#List Server Emojis
@bot.command()
# @commands.cooldown(1,60*60, BucketType.member)
async def serveremoji(ctx, extra='list'):
    """
    List all the custom emoji of the server
    """

    if extra=='list':
        non_animated_list= [f'<:{i.name}:{i.id}>' for i in ctx.guild.emojis if not i.animated]
        animated_list= [f'<a:{i.name}:{i.id}>' for i in ctx.guild.emojis if i.animated]

        if len(non_animated_list)==0 and len(animated_list)==0:
            await ctx.send(f'{ctx.author.mention}\n:exclamation: No custom emojis has been added in this Server.')
        else:
            #NON ANIMATED EMOJIS
            if len(non_animated_list)>0:
                await ctx.send('**Server Emojis**')
                k=0
                non_animated=''
                for i in range(int(len(non_animated_list)/5)+1):
                    non_animated = ' '.join(non_animated_list[k:k+5])
                    k+=5
                    await ctx.send(non_animated)
                    asyncio.sleep(0.4)
            
            #ANIMATED EMOJIS
            if len(animated_list)>0:
                await ctx.send('**Server Animated Emojis**')
                k=0
                animated=''
                for i in range(int(len(animated_list)/5)+1):
                    animated = ' '.join(animated_list[k:k+5])
                    k+=5
                    await ctx.send(animated)
                    asyncio.sleep(0.4)
      
# ========================================================


#Add Reaction to a Message
@bot.command(name='ReactWithEmoji', aliases=['reactemoji', 'remj'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def reactemoji(ctx,  emoji, message: discord.Message= None):

    if not isinstance(message, discord.Message):
        message = ctx.message


    await message.add_reaction(emoji)

# ========================================================


#mass React
@bot.command(name='MassReactWithEmoji', aliases=['massreactemoji', 'mremj'])
@commands.has_any_role('乙乇尺回','ADMIN')
async def massreactemoji(ctx, channel, message, *args):
    channel = bot.get_channel(int(channel))
    message = await channel.fetch_message(int(message))

    for i in args:
        await message.add_reaction(i)

    await ctx.message.add_reaction('☑')

# ========================================================


#send mail
@bot.command(name='MailSend', aliases=['sendmail','smtp'])
async def sendmail(ctx):
    if ctx.author.id == BOT_OWNER_ID:

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            email = environ.get('GMAIL_EMAIL')
            password = environ.get('KHAI_K_HO')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                #target mail address
                await ctx.send('Enter Target Email-Address')
                temp = await bot.wait_for('message', check=check, timeout=30)
                await temp.delete()
                target = temp.content

                if '.' not in target or '@' not in target:
                    await ctx.send('Invalid Email Address')
                    return

                #mail subjct
                await ctx.send('Enter mail subject')
                temp = await bot.wait_for('message', check=check, timeout=50)
                await temp.delete()
                subject = temp.content


                #mail content
                await ctx.send('Enter Content')
                temp = await bot.wait_for('message', check=check, timeout=60)
                await temp.delete()
                content = temp.content

                #confirmation message
                embed = Embed(
                    title='Mail Log',
                    color=random.choice(HEX_COLORS)
                )
                embed.add_field(name='Target', value=target, inline=False)
                embed.add_field(name='Subject', value=subject, inline=False)
                embed.add_field(name='Content', value=content, inline=False)

                embed = await ctx.send(content='Confirm?',embed=embed)
                await embed.add_reaction('☑')
                await embed.add_reaction('❌')

                def check_emj(reaction, user):
                    return user == ctx.author and (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❌')

                #confirm mail send
                reaction, user = await bot.wait_for('reaction_add', check=check_emj, timeout=300)
                await embed.delete()
                reaction = str(reaction)

                if reaction == '☑':

                    # attempt login
                    try:
                        status = await ctx.send(content='Logging in...')
                        smtp.login(email, password)
                    except:
                        await status.edit('Couldnot login. Check the credentials and try again.')
                        return

                    await status.edit(content='Attempting to Send Mail...')
                    msg= f'Subject: {subject}\n\n{content}'
                    smtp.sendmail(email, target, msg)
                    await status.edit(content=f'{ctx.author.mention}\nMail Sent Succssfully!')

                elif reaction == '❌':

                    await ctx.send('Mailing Request Cancelled')
                

            except asyncio.TimeoutError:
                await temp.edit(content='I\'m tired of waiting.')

            except smtplib.SMTPRecipientsRefused:
                await status.edit(content='Invalid Email Address')
            except:
                await ctx.send('Errorrrrr')

# ========================================================


#Bot Announce
@bot.command()
async def announce(ctx, channel:discord.TextChannel):
    if ctx.author.id == BOT_OWNER_ID:
        try:
            await ctx.send('What do you want to announce?')
            content=  await bot.wait_for('message', timeout=300)

            await channel.send(content.content)

        except asyncio.TimeoutError:
            await ctx.send('I can\'t wait any longer')

# ========================================================


#Copy Message And Send
@bot.command()
async def copypaste(ctx, channel: discord.TextChannel, message: discord.Message):
    if ctx.author.id == BOT_OWNER_ID:
        await channel.send(content=message.content, embed=message.embeds[0])

# ========================================================


#create embed
@bot.command()
async def embed(ctx, *content):
    try:
        content= ' '.join(content)

        def check(m):
            return None if m.lower()=='no' else m

        await ctx.send('Any Title?')
        title= (await bot.wait_for('message',timeout=100)).content
        await asyncio.sleep(1)

        await ctx.send('Any Description?')
        description= (await bot.wait_for('message',timeout=100)).content
        await asyncio.sleep(1)

        embed= Embed(
            title=check(title), 
            description=check(description),
            color= random.choice(HEX_COLORS)
        )

        a=True
        def fort(m):
            return False if m.lower()=='false' else True
            
        while a==True:
            await ctx.send('Any Fields?')
            field= await bot.wait_for('message',timeout=100)
            field= str(field.content)

            if field.lower()=='no':
                break

            if '--' not in field:
                return
            
            await asyncio.sleep(1)

            name= (' '.join(field.split('--')[0:1])).strip()
            value= (' '.join(field.split('--')[1:2])).strip()
            inline= fort(field.split('--')[-1].strip())

            embed.add_field(name=name, 
                            value= value, 
                            inline= inline
            )

        await ctx.send(content= content, embed=embed)

    except asyncio.TimeoutError:
        await ctx.send('I can\'t wait any longer')

# ========================================================


#Zer000000000000000000000000000000000
@bot.command(name='Zer00', aliases=['zer0'])
async def zer0(ctx):
    """
    Zeroooooooooo0000000000
    """
    if ctx.author.id == BOT_OWNER_ID:
        a="""
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
        """

        await ctx.send(f'```{a}```')
 
 #========================================================

#Logout the bot
@bot.command(name='LogOutBot', aliases=['logout','close'])
@commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
async def LogOut(ctx):
    """
    Closes The Bot
    """
    if ctx.author.bot == False:
        await ctx.message.add_reaction('☑')
        await ctx.send(f'Bye Bye')
        # memberr = await bot.fetch_user(483179796323631115)
        # await memberr.send(f'Logged Out by: `{ctx.author.name}#{ctx.author.discriminator}` | `{ctx.author.id}` || on `{datetime.utcnow().strftime(datetime.utcnow().strftime("%b %d, %Y | %H:%M:%S"))}`')
        await bot.close()
 
 #========================================================
@bot.command()
async def testbot(ctx):
    wwel = ctx.guild.get_channel(SERVER_CONFIG['welcome_message_channel'])
    await wwel.send('Hello')
    
####Error Handling
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, discord.ext.commands.errors.CommandNotFound):
#         pass
#     elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#         pass
#     elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
#         pass
#     elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
#         await ctx.message.add_reaction('⏳')
#     elif isinstance(error, discord.ext.commands.errors.MissingRole):
#         pass

DISCORD_TOKEN = environ.get('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)

#========================================================  
#========================================================  
