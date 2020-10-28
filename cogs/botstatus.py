import discord
from discord.ext import commands
from time import time
from datetime import datetime


class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='BotPing', aliases=['ping'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _bot_ping(self, ctx):
        """
        Ping the Bot.
        """
        if ctx.author.bot == False:
            start= time()
            message = await ctx.send('**Pinging...**')
            end= time()

            description=f"""
⌛ **Latency:** {int(round(self.bot.latency*1000,1))}ms
\u200b
⏰ **Response Time:** {int((end-start)*1000)}ms
"""
            embed= discord.Embed(
                            color= ctx.author.color, 
                            description=description
                )

            await message.edit(content='',embed=embed)


    @commands.command()
    @commands.is_owner()
    async def uptime(self, ctx):
        """
        Check the Bot's Uptime
        """
        with open('./config/time.txt','r') as f:
            a=f.readline()
            online_time= datetime.strptime(a, "%m/%d/%Y, %H:%M:%S")
            c_time=datetime.now()
            uptime= str(c_time - online_time).split('.')[0] 

        embed= discord.Embed(
                        color= ctx.author.color,
                        description=f'⌛ **UpTime:** {uptime}'
        )
        await ctx.send(embed=embed)


    @commands.command(name='Disconnect', aliases=['logout','close'])
    @commands.is_owner()
    async def LogOut(self, ctx):
        """
        Disconnect The Bot.
        """
        await ctx.message.add_reaction('☑')
        await ctx.send(f'> Disconnected.')
        await self.bot.close()

def setup(bot):
    bot.add_cog(BotStatus(bot))
