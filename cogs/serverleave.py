import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime
import json

class ServerLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        When Someone leaves or are kicked from the Server.
        """
        embed= discord.Embed(
                        color=random.choice(self.bot.hex_colors), 
                        description=f'**{member.name}** has left the server.\nGoodBye:wave:'
            )
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
        embed.timestamp = datetime.utcnow()

        #SEND GOODBYE MESSAGE
        goodybye_channel = member.guild.get_channel(self.bot.SERVER_CONFIG['goodbye_message_channel'])
        goodbye_message = await goodybye_channel.send(embed=embed)

        # EDIT TOTAL MEMBER COUNT
        ctx = await self.bot.get_context(goodbye_message)
        await ctx.invoke(self.bot.get_command('UpdateMemberCount'))

def setup(bot):
    bot.add_cog(ServerLeave(bot))