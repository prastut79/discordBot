"""
A module thats contains the GraphQl
queries of:

1. Series
2. Character
3. Staff
4. Studio
"""


series_query = """\
query ($id: Int!, $type: MediaType) {
    Media(id: $id, type: $type) {
        id
        idMal
        title {
            romaji
            english
            native
        }
        type
        format
        status
        description(asHtml: true)
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
        season
        seasonYear
        seasonInt
        episodes
        duration
        chapters
        volumes
        countryOfOrigin
        isLicensed
        source
        hashtag
        trailer {
            id
            site
            thumbnail
        }
        coverImage {
            extraLarge
            large
            medium
            color
        }
        bannerImage
        genres
        synonyms
        averageScore
        meanScore
        popularity
        isLocked
        trending
        favourites
        tags {
            id
            name
            description
            category
            rank
            isGeneralSpoiler
            isMediaSpoiler
            isAdult
        }
        rankings {
            rank
            type
            allTime
            context
        }
        relations {
            edges {
                id
                node {
                    id
                    siteUrl
                    title {
                        romaji
                        english
                        native
                        userPreferred
                    }
                }
            }
        }
        characters(sort: ROLE) {
            edges {
                id
                node {
                    id
                    siteUrl
                    name {
                        first
                        last
                        full
                        native
                    }
                }
            role
            }
        }
        staff(sort:FAVOURITES_DESC) {
            edges {
                id
                node {
                    id
                    siteUrl
                    name {
                        first
                        last
                        full
                        native
                    }
                }
            }
        }
        studios(isMain: true) {
            nodes {
                name	
            }
        }
        isAdult
        nextAiringEpisode {
            id
            airingAt
            timeUntilAiring
            episode
        }
        externalLinks {
            id
            url
            site
        }
        streamingEpisodes {
            title
            thumbnail
            url
            site
        }
        siteUrl
    }
}

"""


character_query = """\
query ($id: Int!) {
    Character(id: $id) {
        id
        name {
            first
            last
            full
            native
            alternative
        }
        image {
                large
                medium
        }
        description(asHtml: false)
        media(sort: POPULARITY_DESC) {
            edges {
                id
                node {
                    id
                    type
                    siteUrl
                    title {
                        romaji
                        english
                        native
                        userPreferred
                    }
                }
            }
        }
        favourites
        siteUrl
    }
}
"""


staff_query = """\
 
query ($id: Int!) {

    Staff(id: $id) {
        id
        name {
            first
            last
            full
            native
            alternative
        }
        image {
            large
            medium
        }
        language
        description
        favourites
        siteUrl
        staffMedia {
            edges {
                id
                node {
                    id
                    siteUrl
                    title {
                        romaji
                        english
                        native
                        userPreferred
                    }
                }
                staffRole
            }
        }
        characters(sort:FAVOURITES_DESC) {
            edges {
                id
                role
                node {
                    id
                    siteUrl
                    name {
                        first
                        last
                        full
                        native
                    }
                }
            }
        }
    }
}
"""


studio_query = """\
query ($id: Int!) {
    Studio(id: $id) {
        id
        name
        siteUrl
        isAnimationStudio
        favourites
        media(sort:POPULARITY_DESC) {
            edges {
                id
                node {
                    id
                    siteUrl
                    title {
                        romaji
                        english
                        native
                        userPreferred
                    }
                }
            }
        }
    }
}
"""
