import discord
from discord.ext import commands
import json
import requests
import os

def manga_info(request_query):
    url= 'https://graphql.anilist.co'

# Search for the input anime name and get the id of the first result
    query = '''
    query ($query: String) {
    Page {
        media(search: $query, type: MANGA) {
            id
        }
    }
    }
    '''

    variables = {
        'query': request_query
    }
    response = requests.post(url, json={'query': query, 'variables': variables})

    search = json.loads(response.content)

    try:
        manga_id = search['data']['Page']['media'][0]['id']
    except IndexError:
        return 'Manga Not Found.'

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
        synonyms
        format
        chapters
        description
        averageScore
        meanScore
        genres
        source
        popularity
        favourites
        bannerImage
        rankings {
            rank
            type
            allTime
            context
        }
        staff(sort:FAVOURITES_DESC) {
            edges {
                node {
                name {
                    full
                }
                }
            }
        }
        siteUrl
    }
    }
    """
    variables = {
        'id': manga_id
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    info = json.loads(response.content)
    
    return info['data']['Media']

class MangaInfo(commands.Cog):
    with open('./config/server_config.json','r') as f:
        SERVER_CONFIG = json.load(f)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= 'MangaInformation', aliases=['manga'])
    @commands.has_role(SERVER_CONFIG['role_anime_id'])
    @commands.cooldown(1,5, commands.BucketType.user)
    async def _manga(self, ctx, *manga_query):
        """
        Display Information about the specified Manga.
        """

        info = manga_info(' '.join(manga_query))

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
                        title= info['title']['romaji'] or info['title']['english'] or info,
                        url= info['siteUrl'],
                        description= description,
                        color= ctx.author.color
        )

        #Synonyms
        synonyms = list(info['synonyms']) or list(info['title']['userPreferred']) or ['-']
        embed.add_field(
                    name= "Synonyms",
                    value= ('; '.join(synonyms)),
                    inline= False
        )
        #Genre
        genre = info['genres'] or ['-']
        embed.add_field(
                    name= 'Genre',
                    value=(', ').join(genre) +'\n\u200b',
                    inline= False
        )
        #-----------------
        
        #Status
        status = info['status'] or '-'
        embed.add_field(
                    name= 'Status',
                    value= (status.replace('_',' ').title())
        )
        #Volumes
        embed.add_field(
                    name= "Chapters",
                    value= info['chapters'] or '-'
        )
        #Author
        try:
            embed.add_field(
                        name='Author',
                        value= info['staff']['edges'][0]['node']['name']['full'] or '-'
            )
        except IndexError:
            embed.add_field(name='Author', value='-', inline=True)
        #-----------------

        #Source
        source = info['source'] or '-'
        embed.add_field(
                    name= "Source",
                    value= source.title()
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
        typ = (f"({info['format'].replace('_',' ').title()})") if not info['type'].lower() == info['format'].lower() else ""
        embed.set_author(
                    name=f"{info['type'].title()} " + typ
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
    bot.add_cog(MangaInfo(bot))