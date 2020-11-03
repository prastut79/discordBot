# https://anilist.co/graphiql
import discord
from discord.ext import commands
import json
import requests
import os

from .AnilistAPI import search


class AnimeInfo(commands.Cog, search.AnilistSearch):
    with open("./config/server_config.json", "r") as f:
        SERVER_CONFIG = json.load(f)

    def __init__(self, bot):
        self.bot = bot
        self.url = "https://graphql.anilist.co"

    @commands.command(name="AnimeInformation", aliases=["anime"])
    @commands.has_role(SERVER_CONFIG["role_anime_id"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _anime(self, ctx, *anime_query):
        """
        Display Information about the specified Anime.
        """
        info = super().anime_search(" ".join(anime_query))
        if not isinstance(info, dict):
            await ctx.send(f"> {info}")
            return

        if info["description"]:
            """Remove html tags"""
            import re

            clean = re.compile("<.*?>")
            description = re.sub(clean, "", info["description"]) + "\n\u200b"
        else:
            description = "-" + "\n\u200b"

        embed = discord.Embed(
            title=info["title"]["romaji"] or info["title"]["english"] or info,
            url=info["siteUrl"],
            description=description,
            color=ctx.author.color,
        )

        # Synonyms
        synonyms = info["synonyms"] or [
            info["title"]["english"] or info["title"]["native"] or "-"
        ]
        embed.add_field(name="Synonyms", value=("｜".join(synonyms)), inline=False)
        # Genre
        genre = info["genres"] or ["-"]
        embed.add_field(
            name="Genre", value=(", ").join(genre) + "\n\u200b", inline=False
        )
        # -----------------

        # Status
        status = info["status"] or "-"
        embed.add_field(name="Status", value=(status.replace("_", " ").title()))
        # Episodes
        embed.add_field(
            name="Episodes",
            value=info["episodes"]
            or (
                info["nextAiringEpisode"]["episode"] - 1
                if info["status"] != "NOT_YET_RELEASED"
                else "-"
            ),
        )
        # Studio
        try:
            embed.add_field(
                name="Studio", value=info["studios"]["nodes"][0]["name"] or "-"
            )
        except IndexError:
            embed.add_field(name="Studio", value="-", inline=True)
        # -----------------

        # Season
        embed.add_field(
            name="Season",
            value=f"{info['season'].title()} {info['seasonYear']}"
            if info["season"] != None
            else "-",
        )
        # Start Date
        if info["startDate"]["day"]:
            start_date = f"{info['startDate']['day']}/{info['startDate']['month']}/{info['startDate']['year']}"
        else:
            start_date = "-"
        embed.add_field(name="Premire Date", value=start_date)
        # End Date
        if info["endDate"]["day"]:
            end_date = f"{info['endDate']['day']}/{info['endDate']['month']}/{info['endDate']['year']}"

        else:
            end_date = "-"
        embed.add_field(name="End Date", value=end_date)
        # -----------------

        # Score
        embed.add_field(
            name="Score", value=info["averageScore"] or info["meanScore"] or "-"
        )
        # Popularity(Members)
        embed.add_field(name="Members", value=info["popularity"] or "-")
        # Favourites
        embed.add_field(name="Favourites", value=info["favourites"] or "-")
        # -----------------

        # Ranking
        rank = dict()
        for i in info["rankings"]:
            if i["allTime"]:
                rank[i["type"]] = i["rank"]

        # Ranking Rated
        isThere = 0
        try:
            embed.add_field(
                name="Rating", value=(f"#{rank['RATED']}" if rank["RATED"] else "-")
            )
            isThere += 1
        except:
            pass

        # Ranking Popular
        try:
            embed.add_field(
                name="Popularity",
                value=(f"#{rank['POPULAR']}" if rank["POPULAR"] else "-"),
            )
            isThere += 1
        except:
            pass

        if isThere > 1:
            embed.add_field(name="\u200b", value="\u200b")
        # -----------------

        # MAIN CHARACTERS
        characters = list()
        if len(info["characters"]["edges"]) > 1:
            for i in info["characters"]["edges"]:
                if i["role"] == "MAIN":
                    characters.append(i["node"]["name"]["full"])
                else:
                    break
        else:
            characters = ["-"]

        embed.add_field(
            name="Main Characters", value=(", ".join(characters)), inline=False
        )

        # Add Footer
        embed.set_footer(
            text=f"Source: Anilist.co",
            icon_url=f"https://anilist.co/img/icons/android-chrome-512x512.png",
        )
        # Add Author
        embed.set_author(
            name=f"{info['type'].title()} ({info['format'].replace('_',' ').upper()})"
        )
        # Add Thumbnail
        embed.set_thumbnail(url=f"{info['coverImage']['extraLarge']}")
        # Add Image
        if info["bannerImage"]:
            embed.set_image(url=info["bannerImage"])

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeInfo(bot))
 
