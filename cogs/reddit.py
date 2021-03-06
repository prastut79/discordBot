import discord
from discord.ext import commands
import random
from datetime import datetime


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name= 'RedditPost', aliases=['reddit'])
    @commands.cooldown(1,7,commands.BucketType.guild)
    async def randompostfromsubreddit(self, ctx, subred='memes',limit=100):
        """
        Search for a random post from the specified Sub-Reddit (Deafult: r/memes).
        """

        await ctx.channel.trigger_typing()
        
        image_formats= (".png", ".jpg", ".jpeg", ".gif")
        try:
            subreddit = self.bot.reddit.subreddit(subred)
            top = subreddit.new(limit= limit)

            all_posts = [x for x in top if not x.stickied]

            rnd_post = random.choice(all_posts)
            rnd_post_link = f'https://www.reddit.com{rnd_post.permalink}'
            urls_post = f'*{rnd_post.url}*\n'

            if not str(rnd_post.url).endswith(image_formats):
                dec_link = f'{rnd_post.selftext}\n\
{urls_post if not rnd_post.url== rnd_post_link else ""}\n\
`⬆ {rnd_post.ups}`  `⬇ {rnd_post.downs}`  `💬 {len(rnd_post.comments)}`   •   \
[r/{str(rnd_post.subreddit)}](https://www.reddit.com/r/{rnd_post.subreddit})'

            else:
                dec_link= f'{rnd_post.selftext}\n\n\
`⬆ {rnd_post.ups}`  `⬇ {rnd_post.downs}`  `💬 {len(rnd_post.comments)}`   •   \
[r/{str(rnd_post.subreddit)}](https://www.reddit.com/r/{rnd_post.subreddit})'

            embed = discord.Embed(
                title= f'{rnd_post.title}',
                url=rnd_post_link,
                color= random.choice(self.bot.hex_colors),
                description= dec_link
            )

            if str(rnd_post.url).endswith(image_formats):
                embed.set_image(url=rnd_post.url)

            embed.set_footer(text=f'by u/{rnd_post.author}  •  {datetime.fromtimestamp(rnd_post.created).strftime("%d/%m/%Y")}',
                            icon_url= subreddit.icon_img)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'> Error while fetching Data.\n> {e}')

def setup(bot):
    bot.add_cog(Reddit(bot))

        