import discord
from discord.ext import commands
from datetime import datetime


class BotEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
                status=discord.Status.idle, 
                activity=discord.Activity(type=discord.ActivityType.watching, name="ANIMEEE")
        )
        print('Bot is Online. GTG')
        with open('./config/time.txt','w') as f:
            time=str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            f.write(time)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            pass
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send(f'> Error\n> {error}')
        elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.message.add_reaction('⏳')
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            pass
        elif isinstance(error, discord.ext.commands.NotOwner):
            pass


def setup(bot):
    bot.add_cog(BotEvent(bot))