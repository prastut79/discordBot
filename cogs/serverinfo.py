import discord
from discord.ext import commands
import asyncio


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="ServerInformation", aliases=['serverinfo', 'si'])
    @commands.cooldown(5,60*60*24, commands.BucketType.guild)
    async def server_info(self, ctx):
        """
        Information about the server.
        """
        if ctx.author.bot == False:
            embed = discord.Embed(title="Server Information",
                            colour=ctx.guild.owner.colour
            )

            embed.set_thumbnail(url=ctx.guild.icon_url)

            statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

            fields =[
                        ("Owner", f'{ctx.guild.owner.mention}', True),
                        ("Region", f'{str(ctx.guild.region).title()}', True),
                        ("Created on", ctx.guild.created_at.strftime("%b %d, %Y "), True),
                        
                        ("Members", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                        ("Roles", len(ctx.guild.roles), True),
                        ("Banned", len(await ctx.guild.bans()), True),

                        ("Emojis", len(ctx.guild.emojis), True),
                        ("Text channels", len(ctx.guild.text_channels), True),
                        ("Voice channels", len(ctx.guild.voice_channels), True),
                        

                        ("\u200b",f"**🟢  {statuses[0]}｜🟠  {statuses[1]}｜🔴  {statuses[2]}｜⚪  {statuses[3]}**", False)
                    ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)
    

    @commands.command(name='ServerEmojis', aliases=['smoji'])
    @commands.cooldown(1,120, commands.BucketType.member)
    async def _serveremoji(self, ctx, extra='list'):
        """
        List all the Custom emoji of the Server.
        """

        if extra=='list':
            non_animated_list= [f'<:{i.name}:{i.id}>' for i in ctx.guild.emojis if not i.animated]
            animated_list= [f'<a:{i.name}:{i.id}>' for i in ctx.guild.emojis if i.animated]

            if len(non_animated_list)==0 and len(animated_list)==0:
                await ctx.send(f'{ctx.author.mention}\n:exclamation: No custom emojis has been added in this Server.')
            else:
                #NON ANIMATED EMOJIS
                if len(non_animated_list)>0:
                    await ctx.send('**Server Emojis**')
                    k=0
                    non_animated=[]
                    temp=''
                    for i in range(int(len(non_animated_list)/5)+1):
                        temp += ' '.join(non_animated_list[k:k+5])+'\n'
                        k+=5
                        if k>24 and k<26:
                            non_animated.append(temp)
                            temp=''
                    non_animated.append(temp)
            
                    for i in non_animated:
                        await ctx.send(i)
    

                #ANIMATED EMOJIS
                if len(animated_list)>0:
                    await ctx.send('**Server Animated Emojis**')
                    k=0
                    animated=[]
                    temp=''
                    for i in range(int(len(animated_list)/5)+1):
                        temp += ' '.join(animated_list[k:k+5])+'\n'
                        k+=5
                        if k>24 and k<26:
                            animated.append(temp)
                            temp=''
                    animated.append(temp)

                    for i in animated:
                        await ctx.send(i)


def setup(bot):
    bot.add_cog(ServerInfo(bot))