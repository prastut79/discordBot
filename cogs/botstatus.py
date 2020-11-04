from time import time
from datetime import datetime, timedelta
import platform
import psutil as psutil
import psycopg2
import math
from time import time

import discord
from discord.ext import commands

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
    @commands.cooldown(1,10, commands.BucketType.member)
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
    @commands.cooldown(1,10, commands.BucketType.member)
    async def zer0(self, ctx):
        """
        Displays bot's Information.
        """

        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        description = \
f"""\
{self.bot.user.name} is a Multi-Purpose bot for your Discord Server.
"""
        embed = discord.Embed(
                    title= f"{self.bot.user.name} Stats",
                    description= f"{description}\n\uFEFF",
                    colour= 0x53fff1
        )

        embed.add_field(name='Guilds', value= f"`{serverCount}`")
        embed.add_field(name='Users', value= f"`{memberCount}`")
        embed.add_field(name='\uFEFF', value= '\uFEFF')



        bot_developer= self.bot.get_user(self.bot.SERVER_CONFIG['bot_owner_id'])
        embed.set_footer(
                text= 'Developed By Netsos', 
                icon_url= bot_developer.avatar_url
        )
        embed.set_thumbnail(url= self.bot.user.avatar_url)
        await ctx.send(embed=embed)




    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_owner()
    async def status(self, ctx):
        """
        Displays the current status of the bot.
        """
        embed = discord.Embed(title='%s - Status' % self.bot.user.name,
                                        color= ctx.author.color)
        proc = psutil.Process()
        with proc.oneshot():
            uptime = timedelta(seconds=round(time() - proc.create_time()))
        try:
            embed.add_field(name='Uptime', value=str(uptime), inline=True)
        except AttributeError:
            embed.add_field(name='Uptime', value='-',
                                    inline=True)

        guilds = str(len(self.bot.guilds))
        embed.add_field(name='Guilds', value=guilds,
                                inline=True)
        users = 0
        for guild in self.bot.guilds:
            users = users + guild.member_count
        embed.add_field(name='Users', value=users,
                                inline=True)

        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        embed.add_field(name='Bot', value= f"v`{self.bot.version}`")
        embed.add_field(name='Python', value= f"v`{pythonVersion}`")
        embed.add_field(name='discord.py', value= f"v`{dpyVersion}`")

        temperature = ''
        try:
            temp = psutil.sensors_temperatures(False)
            if len(temp) > 0:
                core_temp = temp['cpu_thermal']
                temperature = core_temp[0][1]
        except AttributeError:
            temperature = '-'
        system_started = datetime.fromtimestamp(psutil.boot_time()).strftime('%d-%m-%Y %H:%M:%S')
        embed.add_field(name='System',
                                value=f'**OS:** {platform.system()}\n'
                                        f'**Temperature:** {temperature}\n'
                                        f'**Started:** {system_started}',
                                inline=False)
        embed.add_field(name='CPU',
                                value=f'**Usage:** {psutil.cpu_percent(interval=None)} %\n'
                                        f'**Frequency:** {psutil.cpu_freq(percpu=False)[0]} MHz\n'
                                        f'**Cores:** {psutil.cpu_count()}\n',
                                inline=True)
        embed.add_field(name='Memory',
                                value=f'**Usage:** {psutil.virtual_memory()[2]} %\n'
                                        f'**Used:** {math.ceil(psutil.virtual_memory()[3] // 1000000)} MB\n'
                                        f'**Total:** {math.ceil(psutil.virtual_memory()[0] // 1000000)} MB\n',
                                inline=True)
        embed.add_field(name='Disk',
                                value=f'**Usage:** {psutil.disk_usage("/")[3]} %\n'
                                        f'**Used:** {math.ceil(psutil.disk_usage("/")[1] // 1000000)} MB\n'
                                        f'**Total:** {math.ceil(psutil.disk_usage("/")[0] // 1000000)} MB\n',
                                inline=True)
        await ctx.channel.send(embed=embed)


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
