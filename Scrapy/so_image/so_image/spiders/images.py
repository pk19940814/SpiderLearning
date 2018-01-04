# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from ..items import SoImageItem


class ImagesSpider(scrapy.Spider):
    BASE_URL = 'http://image.so.com/zj?ch=art&sn=%s&listtype=new&temp=1'
    index = 0

    name = 'images'
    # allowed_domains = ['images.so.com']
    start_urls = [BASE_URL % 0]

    MAX_DOWNLOAD_NUM = 100

    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))

        image = SoImageItem()
        image['image_urls'] = [info['qhimg_url'] for info in infos['list']]
        # yield {'images_url': [info['qhimg_url'] for info in infos['list']]}
        yield image

        self.index += infos['count']
        print(not (infos['end']) and self.index < self.MAX_DOWNLOAD_NUM)

        if not (infos['end']) and self.index < self.MAX_DOWNLOAD_NUM:
            print("gun!gun!gun")
            yield Request(self.BASE_URL % self.index)
