import discord
from discord.ext import commands

class BotAppreance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name= 'Playing', aliases=['zplaying'])
    @commands.is_owner()
    async def _zplaying(self, ctx, *name):
        """
        Change Bot Activity to Playing.
        """
        name=' '.join(list(name))
        await self.bot.change_presence(
                status=discord.Status.idle, 
                activity= discord.Game(name= name)
        )
        await ctx.message.add_reaction('☑')

    @commands.command(name= 'Streaming', aliases=['zstreaming'])
    @commands.is_owner()
    async def _zstreaming(self, ctx, url, *name):
        """
        Change Bot Activity to Streaming.
        """
        name = ' '.join(list(name))
        await self.bot.change_presence(
                status=discord.Status.idle,
                activity=discord.Streaming(name= name,  url=url)
        )
        await ctx.message.add_reaction('☑')

    @commands.command(name= 'Watching', aliases=['zwatching'])
    @commands.is_owner()
    async def _zwatching(self, ctx, *name):
        """
        Change Bot Activity to Watching.
        """
        name= ' '.join(list(name))
        await self.bot.change_presence(  
                status=discord.Status.idle, 
                activity=discord.Activity(type=discord.ActivityType.watching, name=name)
        )
        await ctx.message.add_reaction('☑')

    @commands.command(name= 'Listening', aliases=['zlistening'])
    @commands.is_owner()
    async def _zlistening(self, ctx, *name):
        """
        Change Bot Activity to Listening.
        """
        name=' '.join(list(name))
        await self.bot.change_presence(
                status=discord.Status.idle, 
                activity=discord.Activity(type=discord.ActivityType.listening, name=name)
        )
        await ctx.message.add_reaction('☑')
    
def setup(bot):
    bot.add_cog(BotAppreance(bot))

