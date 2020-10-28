#https://discordpy.readthedocs.io/en/latest/logging.html
#whitespace = \u200b 
import os
import json
from datetime import datetime

import discord
from discord.ext import commands

with open('./config/server_config.json','r') as f:
    SERVER_CONFIG = json.load(f)

intents = discord.Intents.all()

SERVER_PREFIX = tuple(SERVER_CONFIG['server_prefixs'])

bot = commands.Bot(command_prefix= SERVER_PREFIX, case_insensitive=True, intents=intents)
# bot.remove_command('help')


#bot Start
@bot.event
async def on_ready():
    await bot.change_presence(
            status=discord.Status.idle, 
            activity=discord.Activity(type=discord.ActivityType.watching, name="ANIMEEE")
    )
    print('Bot is Online. GTG')
    with open('./config/time.txt','w') as f:
        time=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        f.write(time)

@bot.command()
async def load(ctx, extension):
    """
    Load an Extension.
    """
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    """
    Unload an Extension.
    """
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        pass
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        pass
    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.message.add_reaction('⏳')
    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        pass
    elif isinstance(error, discord.ext.commands.NotOwner):
        pass

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(DISCORD_TOKEN)

#========================================================  
#========================================================  
