# -*- coding: utf-8 -*-
import scrapy


class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/']

    def parse(self, response):
        pass
