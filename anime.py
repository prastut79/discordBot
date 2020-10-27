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
    print(search)

    anime_id = search['data']['Page']['media'][0]['id']
        


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
    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    info = json.loads(response.content)
    # print(info)
    return info['data']['Media']

# a= anime_info('boruto naruto next gen')
# s= json.dumps(a, indent=2)
# print(s)
    
