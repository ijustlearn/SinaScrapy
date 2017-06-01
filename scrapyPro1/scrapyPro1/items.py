# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapypro1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Info(scrapy.Item):
    id = scrapy.Field()
    fanstotal = scrapy.Field()
    name  = scrapy.Field()
    sex = scrapy.Field()
    city = scrapy.Field()
    desc = scrapy.Field()#简介
    school = scrapy.Field()
    level = scrapy.Field()
    createDate = scrapy.Field()