# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_si = scrapy.Field()
    title_en = scrapy.Field()
    artist_si = scrapy.Field()
    artist_en = scrapy.Field()
    lyrics_content = scrapy.Field()
    lyrics_raw = scrapy.Field()
    author = scrapy.Field()
#     date = scrapy.Field()
#     downloads = scrapy.Field()
#     plays = scrapy.Field()
#     size = scrapy.Field()

