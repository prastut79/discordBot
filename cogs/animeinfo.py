import discord
from discord.ext import commands
import json
import requests
import os

def anime_info(request_query):
    url= 'https://graphql.anilist.co'

# Search for the input anime name and get the id of the first result
    query = '''
    query ($query: String) {
    Page {
        media(search: $query, type: ANIME) {
            id
            title {
                userPreferred
            }
        }
    }
    }
    '''

    variables = {
        'query': request_query
    }
    response = requests.post(url, json={'query': query, 'variables': variables})

    search = json.loads(response.content)
 
    # animes = [x['title']['userPreferred'] for x in search['data']['Page']['media']]
    # anime_ids = [x['id'] for x in search['data']['Page']['media']]
    # anime_info = dict(zip(animes, anime_ids))
    # anime_id = anime_info[get_close_matches(request_query, animes)[0]]
    try:
        anime_id = search['data']['Page']['media'][0]['id']
    except IndexError:
        return 'Anime Not Found.'

        


# Get the info of the anime from the ID 
    query="""
    query ($id: Int!, $type: MediaType) {
    Media(id: $id, type: $type) {
        id
        title {
            romaji
            english
            native
            userPreferred
        }
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        coverImage {
            large
        }
        status
        type
        episodes
        season
        synonyms
        format
        seasonYear
        description
        averageScore
        meanScore
        genres
        popularity
        favourites
        trailer {
            id
            site
        }
        bannerImage
        rankings {
            rank
            type
            allTime
            context
        }
        nextAiringEpisode {
            episode
        }
        studios(isMain: true) {
            nodes {
                name	
            }
        }
        siteUrl
    }
    }
    """
    variables = {
        'id': anime_id
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    info = json.loads(response.content)
    
    return info['data']['Media']

class AnimeInfo(commands.Cog):
    with open('./config/server_config.json','r') as f:
        SERVER_CONFIG = json.load(f)

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(SERVER_CONFIG['role_anime_id'])
    @commands.cooldown(1,5, commands.BucketType.user)
    async def animeinfo(self, ctx, *anime_query):
        """
        Display Information about the specified Anime.
        """
        info = anime_info(' '.join(anime_query))
        if not isinstance(info,dict):
            await ctx.send(f"> {info}")
            return

        if info['description']:
            """Remove html tags"""
            import re
            clean = re.compile('<.*?>')
            description= re.sub(clean, '', info['description'])+'\n\u200b'
        else:
            description= '-'+'\n\u200b'

        embed= discord.Embed(
                        title=info['title']['romaji'],
                        url= info['siteUrl'],
                        description= description,
                        color= ctx.author.color
        )

        #Synonyms
        embed.add_field(
                    name= "Synonyms",
                    value= ('; '.join(info['synonyms']) or info['title']['userPreferred'] or '-'),
                    inline= False
        )
        #Genre
        embed.add_field(
                    name= 'Genre',
                    value=(f"{(', ').join(info['genres'])}" or '-')+'\n\u200b',
                    inline= False
        )
        #-----------------
        
        #Status
        embed.add_field(
                    name= 'Status',
                    value= (info['status'].replace('_',' ').title() or '-')
        )
        #Episodes
        embed.add_field(
                    name= "Episodes",
                    value= info['episodes'] or (info['nextAiringEpisode']['episode']-1 if info['status'] != 'NOT_YET_RELEASED' else '-')
        )
        #Studio
        try:
            embed.add_field(
                        name='Studio',
                        value= info['studios']['nodes'][0]['name'] or '-'
            )
        except IndexError:
            embed.add_field(name='Studio', value='-', inline=True)
        #-----------------

        #Season
        embed.add_field(
                    name= "Season",
                    value= f"{info['season'].title()} {info['seasonYear']}" if info['season'] != None else '-'
        )
        #Start Date
        if info['startDate']['day']:
            start_date= f"{info['startDate']['day']}/{info['startDate']['month']}/{info['startDate']['year']}"
        else:
            start_date = '-'
        embed.add_field(
                    name= 'Premire Date',
                    value= start_date
        )
        #End Date
        if info['endDate']['day']:
            end_date= f"{info['endDate']['day']}/{info['endDate']['month']}/{info['endDate']['year']}"
            
        else:
            end_date = '-'
        embed.add_field(
                    name= 'End Date',
                    value= end_date 
        )
        #-----------------

        #Score
        embed.add_field(
                    name= "Score",
                    value= info['averageScore'] or info['meanScore'] or '-'
        )
        #Popularity(Members)
        embed.add_field(
                    name= "Members",
                    value= info['popularity'] or '-'
        )
        #Favourites
        embed.add_field(
                    name= "Favourites",
                    value= info['favourites'] or '-'
        )
        #-----------------

        #Ranking
        rank = dict()
        for i in info['rankings']:
            if i['allTime']:
                rank[i['type']] = i['rank']
                
        #Ranking Rated
        isThere=0
        try:
            embed.add_field(
                        name= "Rating",
                        value= (f"#{rank['RATED']}" if rank['RATED'] else '-')
            )
            isThere+=1
        except:
            pass

        #Ranking Popular
        try:
            embed.add_field(
                        name= "Popularity",
                        value= (f"#{rank['POPULAR']}" if rank['POPULAR'] else '-')
            )
            isThere+=1
        except:
            pass
        
        if isThere >1:
            embed.add_field(
                        name= "\u200b",
                        value= "\u200b"
            )
        #-----------------
        
        #Add Footer 
        embed.set_footer(
                    text=f"Source: Anilist.co",
                    icon_url= f"https://anilist.co/img/icons/android-chrome-512x512.png"
        )
        #Add Author 
        embed.set_author(
                    name=f"{info['type'].title()} ({info['format'].upper()})"
        )
        #Add Thumbnail
        embed.set_thumbnail(
                    url=f"{info['coverImage']['large']}"
            )
        #Add Image
        if info['bannerImage']:
            embed.set_image(
                    url=info['bannerImage']
            )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeInfo(bot))