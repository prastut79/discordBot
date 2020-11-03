"""
AnilistSearch Class
~~~~~~~~~~~~~~~~~~~

A class that returns Information 
based on the argument that can be
either ID of the Anime or a
Search query of the following
Attributes:

1. Anime
2. Manga
3. Characters
4. Staff
5. Studio

Incase of the ID ,the method directly
callsthe respective method of Anilist
Class imported from anilist.

Incase of a Search Query, it uses the
query provided to search the Anilist
database and provide the ID of the
best result and then finally call
the respective method of Anilist Class
imported from anilist.

The class raises IllegalArgumentError
if the query does not have any match
in the Anilist Database.

Netsos
"""

import requests
import json

from . import anilist


class IllegalArgumentError(ValueError):
    def __init__(self, name: str):
        super().__init__(f"{name} not Found.")


class AnilistSearch(anilist.Anilist):
    def __init__(self):
        self.url = "https://graphql.anilist.co"

    def anime_search(self, search):
        """
        A Method that returns Anime Info
        based on the given ID or Search Query.
        """
        id = None
        if isinstance(search, str):

            query = """
            query ($query: String) {
                Page {
                    media(search: $query, type: ANIME) {
                        id
                    }
                }
            }
            """
            variables = {"query": search}
            response = requests.post(
                self.url, json={"query": query, "variables": variables}
            )

            info = json.loads(response.text)

            if len(info["data"]["Page"]["media"]) == 0:
                raise IllegalArgumentError("Anime")
            else:
                id = info["data"]["Page"]["media"][0]["id"]

        elif isinstance(search, int):
            id = search
        else:
            raise TypeError('Invalid Argument.')

        return super().series(id)

    def manga_search(self, search):
        """
        A Method that returns Mange Info
        based on the given ID or Search Query.
        """
        id = None

        if isinstance(search, str):
            query = """
            query ($query: String) {
                Page {
                    media(search: $query, type: MANGA) {
                        id
                    }
                }
            }
            """
            variables = {"query": search}
            response = requests.post(
                self.url, json={"query": query, "variables": variables}
            )

            info = json.loads(response.text)

            if len(info["data"]["Page"]["media"]) == 0:
                raise IllegalArgumentError("Manga")
            else:
                id = info["data"]["Page"]["media"][0]["id"]

        elif isinstance(search, int):
            id = search
        else:
            raise TypeError('Invalid Argument.')

        return super().series(id)

    def character_search(self, search):
        """
        A Method that returns Character Info
        based on the given ID or Search Query.
        """
        id = None

        if isinstance(search, str):
            query = """
            query ($query: String) {
                Page {
                    characters(search: $query) {
                        id
                    }
                }
            }
            """
            variables = {"query": search}
            response = requests.post(
                self.url, json={"query": query, "variables": variables}
            )

            info = json.loads(response.text)

            if len(info["data"]["Page"]["characters"]) == 0:
                raise IllegalArgumentError("Character")
            else:
                id = info["data"]["Page"]["characters"][0]["id"]

        elif isinstance(search, int):
            id = search
        else:
            raise TypeError('Invalid Argument.')
        
        return super().character(id)

    def staff_search(self, search):
        """
        A Method that returns Staff Info
        based on the given ID or Search Query.
        """
        id = None

        if isinstance(search, str):
            query = """
            query ($query: String) {
                Page {
                    staff(search: $query) {
                        id
                    }
                }
            }
            """
            variables = {"query": search}
            response = requests.post(
                self.url, json={"query": query, "variables": variables}
            )

            info = json.loads(response.text)

            if len(info["data"]["Page"]["studios"]) == 0:
                raise IllegalArgumentError("Staff")
            else:
                id = info["data"]["Page"]["staff"][0]["id"]

        elif isinstance(search, int):
            id = search
        else:
            raise TypeError('Invalid Argument.')

        return super().staff(id)

    def studio_search(self, search):
        """
        A Method that returns Studio Info
        based on the given ID or Search Query.
        """
        id = None

        if isinstance(search, str):
            query = """
            query ($query: String) {
                Page {
                    studios(search: $query) {
                        id
                    }
                }
            }
            """
            variables = {"query": search}
            response = requests.post(
                self.url, json={"query": query, "variables": variables}
            )
            info = json.loads(response.text)

            if len(info["data"]["Page"]["studios"]) == 0:
                raise IllegalArgumentError("Studio")
            else:
                id = info["data"]["Page"]["studios"][0]['id']

        elif isinstance(search, int):
            id = search
        else:
            raise TypeError('Invalid Argument.')

        return super().studio(id)


# a = AnilistSearch()
# inf = json.dumps(a.studio('mappa'), indent=2)
# print(inf)
