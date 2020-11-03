# https://discordpy.readthedocs.io/en/latest/logging.html
# whitespace = \u200b
import os
import json
from datetime import datetime, timedelta
import praw
import discord
from discord.ext import commands


with open("./config/server_config.json", "r") as f:
    SERVER_CONFIG = json.load(f)

intents = discord.Intents.all()

SERVER_PREFIX = SERVER_CONFIG["server_prefix"]

# def get_prefix(bot, message):
#     id = message.guild.id
#     return commands.when_mentioned_or()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(SERVER_PREFIX, "z!"),
    case_insensitive=True,
    intents=intents,
)
# bot.remove_command('help')

with open("./config/server_config.json", "r") as f:
    bot.SERVER_CONFIG = json.load(f)

bot.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}
bot.hex_colors = [c for c in bot.colors.values()]

bot.version = "2.0"

reddit = praw.Reddit(
    client_id=SERVER_CONFIG["reddit_client_id"],
    client_secret=os.environ.get("reddit_client_secret"),
    username=SERVER_CONFIG["reddit_username"],
    password=os.environ.get("reddit_password"),
    user_agent=SERVER_CONFIG["reddit_user_agent"],
)
bot.reddit = reddit


@bot.command()
async def load(ctx, extension):
    """
    Load an Extension.
    """
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"> Sucessfully Loaded `{extension}`.")


@bot.command()
async def unload(ctx, extension):
    """
    Unload an Extension.
    """
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"> Sucessfully Unloaded `{extension}`.")


@bot.command()
async def reload(ctx, extension):
    """
    Reload an Extension.
    """
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"> Sucessfully Reloaded `{extension}`.")


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN)
