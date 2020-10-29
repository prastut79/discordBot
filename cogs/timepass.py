import discord
from discord.ext import commands
import asyncio
import random


class TimePass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='Choice', aliases=['choose','chs'])
    @commands.cooldown(1,3, commands.BucketType.member)
    async def _choice(self, ctx, *args):
        """
        Choose between different items.
        """
        await ctx.send(f'> {random.choice(args)}')

    @commands.command(name='RollNumber', aliases=['roll'])
    @commands.cooldown(1,3, commands.BucketType.member)
    async def _roll(self, ctx, a=9, b=0):
        """
        Roll a random number between the specified interval.(Deafult 0-100)
        """
        try:
            a=int(a)
            b=int(b)
            if a>b:
                a,b= b,a

            await ctx.send(f'> {random.randint(a,b)}')
        except:
            pass

    @commands.command(name='RepeatUser', aliases=['say','repeat'])
    @commands.cooldown(1,3, commands.BucketType.member)
    async def say(self, ctx, *message):
        """
        Repeat The User.
        """
        
        if ctx.author.bot == False:
            
            if message[0][0] == '-':
                
                try:
                    count=message[0][1]
                    for i in range(int(count)):
                        send=' '.join(list(message)[1:])
                        await ctx.send(send)
                        await asyncio.sleep(0.5)
                except:
                    send=' '.join(list(message))
                    await ctx.send(send)
            else:
                send=' '.join(list(message))
                await ctx.send(send)

def setup(bot):
    bot.add_cog(TimePass(bot))
