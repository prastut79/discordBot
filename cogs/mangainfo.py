import discord
from discord.ext import commands
import json
import requests
import os
import random

from .AnilistAPI import search, errors


class MangaInfo(commands.Cog, search.AnilistSearch):
    with open("./config/server_config.json", "r") as f:
        SERVER_CONFIG = json.load(f)

    def __init__(self, bot):
        self.bot = bot
        self.url = "https://graphql.anilist.co"

    @commands.command(name="MangaInformation", aliases=["manga"])
    # @commands.has_role(SERVER_CONFIG["role_anime_id"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _manga(self, ctx, *manga_query):
        """
        Display Information about the specified Manga.
        """
        manga_query = " ".join(manga_query)
        try:
            manga_query = int(manga_query)
        except ValueError:
            pass
        
        info = super().manga_search(manga_query)
        # try:
            
        # except errors.ContentNotFoundError:
        #     await ctx.send(f"> Manga  `{manga_query}`  Not Found.")
        #     return
        # except errors.IDNotFoundError:
        #     await ctx.send(f"> Manga ID `{manga_query}` Not Found.")
        #     return

        if not isinstance(info, dict):
            await ctx.send(f"> {info}")
            return

        if info["description"]:
            description = info["description"] + "\n\u200b"
        else:
            description = "-" + "\n\u200b"

        embed = discord.Embed(
            title=info["title"]["romaji"] or info["title"]["english"] or info,
            url=info["siteUrl"],
            description=description,
            color= random.choice(self.bot.hex_colors)
        )

        # Synonyms
        synonyms = info["synonyms"] or [
            info["title"]["english"] or info["title"]["native"] or "-"
        ]
        embed.add_field(name="Synonyms", value=("**｜**".join(synonyms)), inline=False)
        # Genre
        genre = info["genres"] or ["-"]
        embed.add_field(
            name="Genre", value=(", ").join(genre) + "\n\u200b", inline=False
        )
        # -----------------

        # Status
        status = info["status"] or "-"
        embed.add_field(name="Status", value=(status.replace("_", " ").title()))
        # Volumes
        embed.add_field(name="Chapters", value=info["chapters"] or "-")
        # Author
        try:
            embed.add_field(
                name="Author",
                value=info["staff"]["edges"][0]["node"]["name"]["full"] or "-",
            )
        except IndexError:
            embed.add_field(name="Author", value="-", inline=True)
        # -----------------

        # Source
        source = info["source"] or "-"
        embed.add_field(name="Source", value=source.title())
        # Start Date
        if info["startDate"]["year"]:
            start_date = f"{info['startDate']['day'] or '?'}-{info['startDate']['month'] or '?'}-{info['startDate']['year']}"
        else:
            start_date = "-"
        embed.add_field(name="Premire Date", value=start_date)
        # End Date
        if info["endDate"]["year"]:
            end_date = f"{info['endDate']['day'] or '?'}-{info['endDate']['month'] or '?'}-{info['endDate']['year']}"

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
            icon_url= self.bot.SERVER_CONFIG['anilist_logo'],
        )
        # Add Author
        typ = (
            (f"({info['format'].replace('_',' ').title()})")
            if not info["type"].lower() == info["format"].lower()
            else ""
        )
        embed.set_author(name=f"{info['type'].title()} " + typ)
        # Add Thumbnail
        embed.set_thumbnail(url=f"{info['coverImage']['extraLarge']}")
        # Add Image
        if info["bannerImage"]:
            embed.set_image(url=info["bannerImage"])

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MangaInfo(bot))
