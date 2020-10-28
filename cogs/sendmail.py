import discord
from discord.ext import commands
import json
import smtplib
import asyncio
from os import environ

class SendMail(commands.Cog):
    with open('./config/server_config.json','r') as f:
        SERVER_CONFIG = json.load(f)


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='SendEMail', aliases=['sendmail','smtp'])
    @commands.is_owner()
    async def sendmail(self, ctx):
        """
        Send a E-Mail
        """
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            email = self.SERVER_CONFIG['gmail_email']
            password = environ.get('KHAI_K_HO')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                #target mail address
                await ctx.send('Enter Target Email-Address')
                temp = await self.bot.wait_for('message', check=check, timeout=30)
                await temp.delete()
                target = temp.content

                if '.' not in target or '@' not in target:
                    await ctx.send('Invalid Email Address')
                    return

                #mail subjct
                await ctx.send('Enter mail subject')
                temp = await self.bot.wait_for('message', check=check, timeout=50)
                await temp.delete()
                subject = temp.content


                #mail content
                await ctx.send('Enter Content')
                temp = await self.bot.wait_for('message', check=check, timeout=60)
                await temp.delete()
                content = temp.content

                #confirmation message
                embed = discord.Embed(
                    title='Mail Log',
                    color= ctx.author.color
                )
                embed.add_field(name='Target', value=target, inline=False)
                embed.add_field(name='Subject', value=subject, inline=False)
                embed.add_field(name='Content', value=content, inline=False)

                embed = await ctx.send(content='Confirm?',embed=embed)
                await embed.add_reaction('☑')
                await embed.add_reaction('❌')

                def check_emj(reaction, user):
                    return user == ctx.author and (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❌')

                #confirm mail send
                reaction, user = await self.bot.wait_for('reaction_add', check=check_emj, timeout=300)
                await embed.delete()
                reaction = str(reaction)

                if reaction == '☑':

                    # attempt login
                    try:
                        status = await ctx.send(content='Logging in...')
                        smtp.login(email, password)
                    except:
                        await status.edit('Couldnot login. Check the credentials and try again.')
                        return

                    await status.edit(content='Attempting to Send Mail...')
                    msg= f'Subject: {subject}\n\n{content}'
                    smtp.sendmail(email, target, msg)
                    await status.edit(content=f'{ctx.author.mention}\nMail Sent Succssfully!')

                elif reaction == '❌':

                    await ctx.send('Mailing Request Cancelled')
                

            except asyncio.TimeoutError:
                await temp.edit(content='I\'m tired of waiting.')

            except smtplib.SMTPRecipientsRefused:
                await status.edit(content='Invalid Email Address')
            except:
                await ctx.send('Errorrrrr')

def setup(bot):
    bot.add_cog(SendMail(bot))
