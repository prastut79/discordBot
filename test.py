# import csv
# import json
# import datetime
import random
# import string
# # import os
# import string
# import datetime
# # from typing import Optional
# # import emoji
# import os 
# import praw



# import discords
# from discord import Embed, Member
# from discord.ext.commands import Cog
# from discord.ext.commands import command
# from time import time
# import selenium

def anime_info(request_query):
    url = "https://graphql.anilist.co"

    # Search for the input anime name and get the id of the first result
    query = """
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
    """

    variables = {"query": request_query}
    response = requests.post(url, json={"query": query, "variables": variables})

    search = json.loads(response.content)

    try:
        anime_id = search["data"]["Page"]["media"][0]["id"]
    except IndexError:
        return "Anime Not Found."

    # Get the info of the anime from the ID
    query = """
    query ($id: Int!, $type: MediaType) {
        Media(id: $id, type: $type) {
            id
            idMal
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
                extraLarge
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
            characters(sort: ROLE){ 
                edges {
                    node {
                        name {
                            full
                        }
                    }
                    role
                }
            }
        }
    }
    """
    variables = {"id": anime_id}
    response = requests.post(url, json={"query": query, "variables": variables})
    info = json.loads(response.content)

    return info["data"]["Media"]
