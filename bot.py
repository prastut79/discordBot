#https://discordpy.readthedocs.io/en/latest/logging.html

import discord
from discord.ext import commands
from random import choice
import os

bot = commands.Bot(command_prefix='>')

#bot Start
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Watching ANIMEE'))
    print('Bot is ready')


#Serve Join
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


#Server Leave
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


#Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping: {int(round(bot.latency*1000,1))}ms')

#Hello Command
@bot.command(aliases=['hello','hi'])
async def _hello(ctx ):
    responses=[ 
        'Hey',
        'Hi', 
        'Hello',
        'How are you?',
        'How’s it going',
        'Konichiwa'
    ]
    await ctx.send(choice(responses))

#Bye Command
@bot.command(aliases=['bye','byebye'])
async def _bye(ctx):
    responses=[
        'Bye',
        'bye',
        'Bye. See ya',
        'See you around'
    ]
    await ctx.send(choice(responses))


#Clear Message Command
@bot.command()
@commands.has_any_role('乙乇尺回','MODs','ADMIN','GUYzz')
async def clear(ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} messages')
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Sorry you are not allowed to use this command.')
    

bot.run('NzU2ODE2NTEzMDM3NzYyNTgx.X2XWTQ.h-3pujN5KbKbqnDsAhtVq7RRHKQ')
# bot.run(os.environ('DISCORD_TOKEN'))

