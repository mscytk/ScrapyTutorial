# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class BirdfanItem(Item):
    title = Field()
    url = Field()
    jpgurl = Field()
    birdname = Field()

    # class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #    pass
