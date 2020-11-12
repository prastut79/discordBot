import discord
from discord.ext import commands
import requests


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_url(self,query):
        r = requests.get(f"https://nekos.life/api/v2/img/{query}")
        info = r.json()
        try:
            return info['url']
        except:
            raise ValueError
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def kiss(self, ctx, user: discord.member = 'da'):
        ctx.send('hi')
