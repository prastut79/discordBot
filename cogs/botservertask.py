import discord
from discord.ext import commands
import asyncio


class BotServerTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="Invitaion",aliases=['cinv','invitationlink'])
    @commands.cooldown(1,60, commands.BucketType.member)
    async def inv(self, ctx):
        """
        Create a Invitaion Link for the Server.
        """

        inv_link = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=False)

        await ctx.author.send(f'Here is the Invitation link to This server\n{inv_link}')
        await ctx.message.add_reaction('📥')


    @commands.command(name= 'CreateEmbed', aliases=['embed'])
    @commands.is_owner()
    async def _embed(self, ctx, *content):
        """
        Create An Embed.
        """
        try:
            content= ' '.join(content)

            def check(m):
                return None if m.lower()=='no' else m

            await ctx.send('Any Title?')
            title= (await self.bot.wait_for('message',timeout=100)).content
            await asyncio.sleep(1)

            await ctx.send('Any Description?')
            description= (await self.bot.wait_for('message',timeout=100)).content
            await asyncio.sleep(1)

            embed= discord.Embed(
                title=check(title), 
                description=check(description),
                color= ctx.author.color
            )

            a=True
            def fort(m):
                return False if m.lower()=='false' else True
                
            while a==True:
                await ctx.send('Any Fields?')
                field= await self.bot.wait_for('message',timeout=100)
                field= str(field.content)

                if field.lower()=='no':
                    break

                if '--' not in field:
                    return
                
                await asyncio.sleep(1)

                name= (' '.join(field.split('--')[0:1])).strip()
                value= (' '.join(field.split('--')[1:2])).strip()
                inline= fort(field.split('--')[-1].strip())

                embed.add_field(name=name, 
                                value= value, 
                                inline= inline
                )

            await ctx.send(content= content, embed=embed)

        except asyncio.TimeoutError:
            await ctx.send('I can\'t wait any longer')
        
    @commands.command(name= 'CopyAndPaste', aliases=['copypaste'])
    @commands.is_owner()
    async def _copypaste(self, ctx, channel: discord.TextChannel, message: discord.Message):
        """
        Copy And Paste a Specified Message in a Specified Channel.
        """
        await channel.send(content=message.content, embed=message.embeds[0])
    

    @commands.command(name="DirectMessage", aliases=['dm'])
    @commands.is_owner()
    async def _dm(self, ctx, user:discord.Member, *message):
        """
        DM a User.
        """
        message= ' '.join(list(message))
        await user.send(message)
        await ctx.message.add_reaction('☑')

    @_dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'{ctx.author.mention}\nMember not Found.')

    @commands.command(name='ClearMessages',  aliases=['clear','clearmsg','cls'])
    @commands.has_any_role('乙乇尺回','MOD','ADMIN','GUYZ')
    async def _clear(self, ctx, amount=1):
        """
        Delete Messages.
        """
        if ctx.author.bot == False:
            if amount<100:
                await ctx.channel.purge(limit=amount+1)
            else:
                await ctx.channel.purge(limit=100)


    @commands.command(name='AddReaction', aliases=['mremj'])
    @commands.has_any_role('乙乇尺回','ADMIN')
    async def _addreaction(self, ctx, channel, message, *args):
        """
        Add reactions to a Message.
        """
        channel = self.bot.get_channel(int(channel))
        message = await channel.fetch_message(int(message))

        for i in args:
            await message.add_reaction(i)

        await ctx.message.add_reaction('☑')


    @commands.command(name='Zer00', aliases=['zer0'])
    @commands.is_owner()
    async def zer0(self, ctx):
        """
        Zeroooooooooo0000000000
        """
   
        a="""
                     ,----,                                    
	    	       .'   .`|                  ,----..           
	    	    .'   .'   ;                 /   /   \          
	    	  ,---, '    .'        __  ,-. /   .     :         
	    	  |   :     ./       ,' ,'/ /|.   /   ;.  \        
	    	  ;   | .'  /  ,---. '  | |' .   ;   /  ` ;        
	    	  `---' /  ;  /     \|  |   ,;   |  ; \ ; |        
	    	    /  ;  /  /    /  '  :  / |   :  | ; | '        
	    	   ;  /  /--.    ' / |  | '  .   |  ' ' ' :        
		      /  /  / .`'   ;   /;  : |  '   ;  \; /  |        
		    ./__;       '   |  / |  , ;   \   \  ',  /         
		    |   :     .'|   :    |---'     ;   :    /          
		    ;   |  .'    \   \  /           \   \ .'           
		    `---'         `----'             `---`                                   
        """

        await ctx.send(f'```{a}```')

def setup(bot):
    bot.add_cog(BotServerTask(bot))

    