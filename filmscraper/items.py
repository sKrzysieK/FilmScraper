# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FilmItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    org_title = scrapy.Field()
    length = scrapy.Field()
    year = scrapy.Field()
    avg_viewer_rating = scrapy.Field()
    avg_critic_rating = scrapy.Field()
    plot = scrapy.Field()
    poster_url = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    universum = scrapy.Field()
    world_premiere = scrapy.Field()
    pl_premiere = scrapy.Field()
    photos_url = scrapy.Field()
    video_url = scrapy.Field()
    cast = scrapy.Field()
    direction = scrapy.Field()
    script = scrapy.Field()
    description = scrapy.Field()
    boxoffice = scrapy.Field()
    budget = scrapy.Field()
    studio = scrapy.Field()
    trivia = scrapy.Field()
    viewer_ratings = scrapy.Field()
