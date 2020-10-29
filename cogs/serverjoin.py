import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime
import json

class ServerJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        When Someone joins the Server.
        """
        #WELCOME MESSAGE------------------------------------------------------------
        embed=discord.Embed(color= random.choice(self.bot.hex_colors), 
                            description=f'{member.mention}, Welcome to **{member.guild}**.:tada:\n\nMember **#{len(list(member.guild.members))}**'
            )
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
        embed.timestamp = datetime.utcnow()
        

        #send welcome message
        welcome_message_channel = member.guild.get_channel(self.bot.SERVER_CONFIG['welcome_message_channel'])
        welcome_msg= await welcome_message_channel.send(embed=embed)

        
        #EDIT TOTAL MEMBER COUNT
        member_count_channel = member.guild.get_channel(self.bot.SERVER_CONFIG['member_count_channel'])
        await member_count_channel.edit(name=f'🧑｜MEMBERS: {len(member.guild.members)}')

        #GIVE ROLE ON JOIN
        if member.bot:
            role_bot = discord.utils.get(member.guild.roles, id= self.bot.SERVER_CONFIG.get('role_bot_id'))
            await member.add_roles(role_bot)
        else:
            role_to_give_on_join = self.bot.SERVER_CONFIG['role_to_give_on_join']
            for i in role_to_give_on_join:
                role_to_give_on_join = discord.utils.get(member.guild.roles, id=i)
                await member.add_roles(role_to_give_on_join)
                await asyncio.sleep(1)

            #_--------------------SEND DM---------------------------------------------
            #create inv link
            inv_link = await welcome_message_channel.create_invite(max_age=0, max_uses=0, unique=False)

            welcome_dm = f'''\
Welcome {member.mention}

Have a great time here in **{member.guild}**

Enjoyyyy:tada:
        
Here is the Invitation Link to this Server:
{inv_link}
'''
            #gifs
            with open('config/welcome_gifs.txt','r') as f:
                gifs = f.readlines()
                
            embed= discord.Embed(
                color= random.choice(self.bot.hex_colors),
                description=welcome_dm
                )
            embed.set_image(url=random.choice(gifs))
            await member.send(embed=embed)
            
        #add reaction
        welcome_emoji = discord.utils.get(member.guild.emojis, name='welcome')
        await welcome_msg.add_reaction(welcome_emoji)

def setup(bot):
    bot.add_cog(ServerJoin(bot))
