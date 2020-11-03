"""
Anilist Class
~~~~~~~

A Class that uses the  Anilist API(v2 GraphQL) to get information on:

1. Anime
2. Manga
3. Characters
4. Staff
5. Studio

Raises IllegalArgumentError if the provided ID does not have any
matches in te Anilist Database.

*Unique ID of each of the above Attributes is Required.

Netsos
"""


import requests
import json
import re
from . import query
# import query

class IllegalArgumentError(ValueError):
    def __init__(self):
        super().__init__("No such ID exists in Anilist Database.")


class Anilist:
    def __init__(self):
        self.url = "https://graphql.anilist.co"

    def series(self, id: int):
        """
        This Method takes ID of an Series in the Parameter.

        Returns the Series Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.series_query, "variables": variables}
        )
        if response.status_code == 404:
            raise IllegalArgumentError

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)
        
        if info is None:
            raise IllegalArgumentError
        
        return info["data"]["Media"]

    def character(self, id: int):
        """
        This Method takes ID of a Character in the Parameter.

        Returns the Character Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.character_query, "variables": variables}
        )
        if response.status_code == 404:
            raise IllegalArgumentError

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        if info is None:
            raise IllegalArgumentError

        return info["data"]["Character"]

    def staff(self, id: int):
        """
        This Method takes ID of a Staff in the Parameter.

        Returns the Staff Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.staff_query, "variables": variables}
        )
        if response.status_code == 404:
            raise IllegalArgumentError

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Staff"]

    def studio(self, id: int):
        """
        This Method takes ID of a Studio in the Parameter.

        Returns the Studio Information based on the Provided ID as a Dictionary.
        """
        variables = {"id": id}

        response = requests.post(
            self.url, json={"query": query.studio_query, "variables": variables}
        )
        if response.status_code == 404:
            raise IllegalArgumentError

        # Clearing out the HTML tags
        clean = re.compile("<.*?>")
        response = re.sub(clean, "", response.text)

        info = json.loads(response)

        return info["data"]["Studio"]



# obj = Anilist()

# a=obj.series(105333)
# # # a=obj.staff(95185)
# # # a=obj.studio(79)
# a=json.dumps(a, indent=2)
# print(a)
