# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = 'amazon_listing_info'

    title = Field()
    bullet_points = Field()
    category = Field()
    asin = Field()
    price = Field()
    rating = Field()
    reviews = Field()
    date = Field()
    country = Field()
