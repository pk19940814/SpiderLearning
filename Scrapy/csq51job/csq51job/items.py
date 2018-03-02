# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Csq51JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobInfo(scrapy.Item):
    name = scrapy.Field()  # 工作名称
    area = scrapy.Field()  # 地区
    salary = scrapy.Field()  # 薪酬
    corp_name = scrapy.Field()  # 公司名称
    description = scrapy.Field()  # 简短描述，是否是国企、员工人数与行业类别等等
    job_restrict = scrapy.Field()  # 招聘信息
    welfare = scrapy.Field()  # 福利
