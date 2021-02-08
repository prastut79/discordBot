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
    async def on_command(self, ctx):
        if ctx.message.author == self.bot.user:
            return
        elif isinstance(ctx.message.channel, discord.channel.DMChannel):
            # await ctx.send('u')
            return

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    #         # await ctx.send(f'>>> **Error** {error}')
    #         pass
    #     elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    #         await ctx.send(f'``` **Error** \nMissing Required Argument.\n{error}```')
    #     elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
    #         await ctx.send(f'``` **Error:** {error}```')
    #     elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
    #         await ctx.message.add_reaction('⏳')
    #     elif isinstance(error, discord.ext.commands.errors.MissingRole):
    #         # await ctx.send(f'>>> **Error** {error}')
    #         pass
    #     elif isinstance(error, discord.ext.commands.NotOwner):
    #         # await ctx.send(f'>>> **Error** {error}')
    #         pass
    #     else:
    #         await ctx.send(f'``` **Error:** {error}```')


def setup(bot):
    bot.add_cog(BotEvent(bot))