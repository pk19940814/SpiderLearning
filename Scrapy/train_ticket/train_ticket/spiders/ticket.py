# -*- coding: utf-8 -*-
import scrapy


class TicketSpider(scrapy.Spider):
    name = 'ticket'
    allowed_domains = ['12306.cn']
    start_urls = ['http://12306.cn/']

    def parse(self, response):
        pass
