"""
Errors
~~~~~~


Error for AnilistAPI

@Netsos
"""


allErrors = ("IdNotFoundError", "ContentNotFound")


class IDNotFoundError(ValueError):
    """
    isRaised if the provided ID does not have any
    matches in te Anilist Database.
    """

    def __init__(self, name):
        super().__init__(f"No {name} found with such ID.")


class ContentNotFoundError(ValueError):
    """
    isRaised if the query does not have any match
    in the Anilist Database.
    """

    def __init__(self, name: str):
        super().__init__(f"{name} not Found.")
