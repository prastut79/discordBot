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

with open('./config/server_config.json','r') as f:
    bot.SERVER_CONFIG = json.load(f)

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.hex_colors = [c for c in bot.colors.values()]

bot.version = '2.0'

@bot.command()
async def load(ctx, extension):
    """
    Load an Extension.
    """
    bot.load_extension(f"cogs.{extension}")
    ctx.send(f"> Sucessfully Loaded `{extension}`")

@bot.command()
async def unload(ctx, extension):
    """
    Unload an Extension.
    """
    bot.unload_extension(f"cogs.{extension}")
    ctx.send(f"> Sucessfully Unloaded `{extension}`")



if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")

    DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
    bot.run(DISCORD_TOKEN)

