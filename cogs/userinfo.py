import discord
from discord.ext import commands
import asyncio


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="UserInformation", aliases=["userinfo", "ui"])
    @commands.cooldown(1,5, commands.BucketType.member)
    async def _user_info(self, ctx, target: discord.Member= None):
        """
        Information about the User.
        """
        if ctx.author.bot == False:
            target = target or ctx.author

            embed = discord.Embed(title= target.name,
                            colour=target.colour)

            embed.set_thumbnail(url=target.avatar_url)
            status={
                'idle': '🟠',
                'online' : '🟢',
                'dnd': '🔴',
                'offline': '⚪'
            }

            if target.activity.type== discord.ActivityType.custom or target.activity.type==None:
                activity_type = ''
            else:
                activity_type = str(target.activity.type).split('.')[-1].title()

            activity= f"{status[str(target.status)]}  {activity_type} {target.activity.name if target.activity else ''}"
            
            fields = [
                        ('Nickname', str(target.nick) if target.nick else '-',True),
                        ("Top role", target.top_role.mention, True),
                        ("Joined on", target.joined_at.strftime("%b %d, %Y "), False)
            ]
                        
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            embed.set_footer(text= activity)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))