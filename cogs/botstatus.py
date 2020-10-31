import discord
from discord.ext import commands
from time import time
from datetime import datetime
import platform

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
        Check the Bot's Uptime.
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

    @commands.command(name= 'ServerPrefix', aliases=['prefix'])
    async def _prefix(self, ctx):
        """
        Display the Bot's Prefix in the Server.
        """
        embed= discord.Embed(
            description= f"My Prefix in this Server are  `z!`  and  `-`",
            color= ctx.author.color
        )
        await ctx.send(embed= embed)

    @commands.command()
    async def stats(self, ctx):
        """
        Displays bot's statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
                    title= f"{self.bot.user.name} Stats",
                    description= '\uFEFF',
                    colour= 0x53fff1
        )

        
        embed.add_field(name='Guilds', value= f"`{serverCount}`")
        embed.add_field(name='Users', value= f"`{memberCount}`")
        embed.add_field(name='\uFEFF', value= '\uFEFF')
        embed.add_field(name='Bot', value= f"`{self.bot.version}`")
        embed.add_field(name='Python', value= f"`{pythonVersion}`")
        embed.add_field(name='discord.py', value= f"`{dpyVersion}`")

        embed.set_footer(
                text= 'Developed By Netsos', 
                icon_url= ''
        )
        embed.set_thumbnail(url= self.bot.user.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(name='Disconnect', aliases=['logout','close'])
    @commands.is_owner()
    async def LogOut(self, ctx):
        """
        Disconnect The Bot.
        """
        await ctx.message.add_reaction('☑')
        await ctx.send(f'> :wave: Disconnected. ')
        await self.bot.close()

def setup(bot):
    bot.add_cog(BotStatus(bot))
