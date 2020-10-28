import discord
from discord.ext import commands
import asyncio


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="UserInformation", aliases=["userinfo", "ui"])
    @commands.cooldown(2,10, commands.BucketType.member)
    async def _user_info(self, ctx, target: discord.Member= None):
        """
        Information about the User.
        """
        if ctx.author.bot == False:
            target = target or ctx.author

            embed = discord.Embed(title="User Information",
                            colour=target.colour)

            embed.set_thumbnail(url=target.avatar_url)

            fields = [                    
                        ("Name", f'{str(target)} {"**Bot**" if target.bot else ""}', True),
                        ('Nickname', str(target.nick),True),
                        ("Top role", target.top_role.mention, True),
                        
                        ("Status", str(target.status).title(), True),
                        ("Activity", f"*{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'}* **{target.activity.name if target.activity else ''}**", True),
                        ("Joined at", target.joined_at.strftime("%b %d, %Y "), False)
            ]
                        
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))