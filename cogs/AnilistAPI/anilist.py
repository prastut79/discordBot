"""
Anilist Class
~~~~~~~

A Class that uses the  Anilist API(v2 GraphQL) to get information on:

1. Anime
2. Manga
3. Characters
4. Staff
5. Studio

*Unique ID of each of the above Attributes is Required.

@Netsos
"""


import requests
import json
import re

from . import query
from . import errors


class Anilist:
    def __init__(self):
        self.url = "https://graphql.anilist.co"

    def anime(self, id: int):
        """
        This Method takes ID of an Anime.

        Returns the Series Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.anime_query, "variables": variables}
        )

        if response.status_code == 404 or response.status_code == 400:
            raise errors.IDNotFoundError("Anime")

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Media"]

    def manga(self, id: int):
        """
        This Method takes ID of a Manga.

        Returns the Series Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.manga_query, "variables": variables}
        )

        if response.status_code == 404 or response.status_code == 400:
            raise errors.IDNotFoundError("Manga")

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Media"]

    def character(self, id: int):
        """
        This Method takes ID of a Character.

        Returns the Character Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.character_query, "variables": variables}
        )
        if response.status_code == 404 or response.status_code == 400:
            raise errors.IDNotFoundError("Character")

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Character"]

    def staff(self, id: int):
        """
        This Method takes ID of a Staff.

        Returns the Staff Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.staff_query, "variables": variables}
        )
        if response.status_code == 404 or response.status_code == 400:
            raise errors.IDNotFoundError("Staff")

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Staff"]

    def studio(self, id: int):
        """
        This Method takes ID of a Studio.

        Returns the Studio Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.studio_query, "variables": variables}
        )
        if response.status_code == 404 or response.status_code == 400:
            raise errors.IDNotFoundError("Studio")

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Studio"]
