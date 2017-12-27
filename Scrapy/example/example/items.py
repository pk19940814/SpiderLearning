# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class BookItem(Item):
    name = Field()
    price = Field()


class ForeignBookItem(BookItem):
    translator = Field()
