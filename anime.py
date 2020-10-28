#Api: https://github.com/AniList/ApiV2-GraphQL-Docs/tree/master/migration
import requests
import json
from difflib import get_close_matches


#Anime Info
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
        description
        averageScore
        meanScore
        genres
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
    }
    }
    """
    variables = {
        'id': anime_id
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    info = json.loads(response.content)

    return info['data']['Media']


