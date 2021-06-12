from discord.ext import commands
import discord
from datetime import datetime
import random


class MemberEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.SERVER_CONFIG

    async def on_server_boost(self, member: discord.Member):
        sever_log = member.guild.get_channel(self.config["server_log_channel"])

        embed = discord.Embed(
            color=int(self.config["server_booster_color"], 16),
            description=f"{member.mention} just boosted the server. \n\nBooster: **#{len(member.guild.premium_subscribers)}**",
        )

        embed.set_author(
            name="Booster Added", icon_url=self.config["server_booster_icon"]
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.utcnow()

        await member.add_roles(
            member.guild.get_role(self.config["role_server_boosters"])
        )

        booster_message = await sever_log.send(embed=embed)

        await booster_message.add_reaction(
            await member.guild.fetch_emoji(self.config["server_booster_emoji"])
        )

        message = (
            f"{member.mention}, ThankYou for Boosting the Server: **{member.guild}**"
        )

        tyembed = discord.Embed(
            color=random.choice(self.bot.hex_colors), description=message
        )

        await member.send(embed=tyembed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        When a server Member is updated
        """
        if before.premium_since is None and after.premium_since is not None:
            await self.on_server_boost(after)


def setup(bot):
    bot.add_cog(MemberEvent(bot))
