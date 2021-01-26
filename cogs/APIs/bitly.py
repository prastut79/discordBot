"""
Bit.ly
~~~~~~

A module that uses bit.ly API to customize a Link.

https://dev.bitly.com/api-reference#createBitlink

"""

import requests
import json

class LinkShortenError(ValueError):
    """A Class that handles error during
    shortening links.
    """

    def __init__(self):
        super().__init__('Errorr.')


def shorten_link(token: str, link: str ):

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = str({ "long_url": link, "domain": "bit.ly"})

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
   
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        raise LinkShortenError
  

token = 'c5c9ed81011f10d9e5b87e091468dda5dc579a65'
update_link(token, 'bit.ly/3pO85ZL')

# """  

# # print(shorten_link(token))

# def update_link(token: str, link: str):

#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json',
#     }   

#     data = {

#         "link": "https://bit.ly/documentation", 
#         "id": "bit.ly/documentation", 
#         "long_url": "https://dev.bitly.com", 
#         "title": "Bitly API Documentation", 
#         "archived": false, 
#         "created_at": "2006-03-12T16:29:46 0000", 
#         "created_by": "chauncey", 
#         "client_id": "1234a56b789cd0e123456fg7h8901j123km45n6p", 
#         "custom_bitlinks": [ 
#             "https://chauncey.ly/documentation" 
#         ],
#         "tags": [ 
#             "bitly", 
#             "api" 
#         ], 
#         "deeplinks": [ 
#             {
#                 "guid": "Ra1bcD2eF3h", 
#                 "bitlink": "bit.ly/documentation", 
#                 "app_uri_path": "/store?id': '123456", 
#                 "install_url": "https://play.google.com/store/apps/details?id=com.bitly.app',
#                 'hl': 'en_US", 
#                 "app_guid": "Ab1cdE2fG3h", 
#                 "os": "android", 
#                 "install_type": "promote_install", 
#                 "brand_guid": "Ba1bc23dE4F" 
#             } 
#         ] 
#     }

#     response = requests.patch(f'https://api-ssl.bitly.com/v4/bitlinks/{link}', headers=headers, data=data)
#     print(response.text)
# """

