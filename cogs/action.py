import discord
from discord.ext import commands
import random
import requests


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def get_url(self, query, description):
        r = requests.get(f"https://nekos.life/api/v2/img/{query}")
        info = r.json()
        embed = discord.Embed(
            description= description,
            color= random.choice(self.bot.hex_colors)
        )
        embed.set_image(url = info['url'])
        return embed


    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def gasm(self, ctx, user: discord.Member = None):
        """Gasm Someone.
        """
        description= f"{ctx.author.mention} just Gasmed {user.mention if user else 'Himself'}"
        embed = self.get_url('gasm', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def poke(self, ctx, user: discord.Member = None):
        """Poke Someone.
        """
        description= f"{ctx.author.mention} just Pokeed {user.mention if user else 'Himself'}"
        embed = self.get_url('poke', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def slap(self, ctx, user: discord.Member = None):
        """Slap Someone.
        """
        description= f"{ctx.author.mention} just Slaped {user.mention if user else 'Himself'}"
        embed = self.get_url('slap', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def waifu(self, ctx, user: discord.Member = None):
        """Waifu Someone.
        """
        description= f"{ctx.author.mention} just Waifued {user.mention if user else 'Himself'}"
        embed = self.get_url('waifu', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def pat(self, ctx, user: discord.Member = None):
        """Pat Someone.
        """
        description= f"{ctx.author.mention} just Pated {user.mention if user else 'Himself'}"
        embed = self.get_url('pat', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def kiss(self, ctx, user: discord.Member = None):
        """Kiss Someone.
        """
        description= f"{ctx.author.mention} just Kissed {'😘 '+user.mention if user else 'Himself 😔'}"
        embed = self.get_url('kiss', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def neko(self, ctx, user: discord.Member = None):
        """Neko Someone.
        """
        description= f"{ctx.author.mention} just Nekoed {user.mention if user else 'Himself'}"
        embed = self.get_url('neko', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def spank(self, ctx, user: discord.Member = None):
        """Spank Someone.
        """
        description= f"{ctx.author.mention} just Spanked {user.mention if user else 'Himself'}"
        embed = self.get_url('spank', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def cuddle(self, ctx, user: discord.Member = None):
        """Cuddle Someone.
        """
        description= f"{ctx.author.mention} just Cuddleed {user.mention if user else 'Himself'}"
        embed = self.get_url('cuddle', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def hug(self, ctx, user: discord.Member = None):
        """Hug Someone.
        """
        description= f"{ctx.author.mention} just Huged {user.mention if user else 'Himself'}"
        embed = self.get_url('hug', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def smug(self, ctx, user: discord.Member = None):
        """Smug Someone.
        """
        description= f"{ctx.author.mention} just Smuged {user.mention if user else 'Himself'}"
        embed = self.get_url('smug', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def baka(self, ctx, user: discord.Member = None):
        """Baka Someone.
        """
        description= f"{ctx.author.mention} just Bakaed {user.mention if user else 'Himself'}"
        embed = self.get_url('baka', description)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.cooldown(1,3, commands.BucketType.member)
    async def woof(self, ctx, user: discord.Member = None):
        """Woof Someone.
        """
        description= f"{ctx.author.mention} just Woofed {user.mention if user else 'Himself'}"
        embed = self.get_url('woof', description)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Action(bot))

