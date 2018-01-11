# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
from ..items import Book

lua_script = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end
'''


class JdBooksSpider(scrapy.Spider):
    name = 'jd_books'
    allowed_domains = ['search.jd.com']
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&suggest=1.def.0.V04&book=y&wq=python'

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        total = int(response.css('span#J_resCount::text').extract_first().split('+')[0])
        page_num = total // 60 + (1 if total % 60 else 0)
        for i in range(page_num):
            url = '%s&page=%s' % (self.base_url, 2 * i + 1)
            yield SplashRequest(url,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'])

    def parse(self, response):
        for sel in response.css('ul.gl-warp.clearfix>li.gl-item'):
            book = Book()
            book['name'] = sel.css('div.p-name').xpath('string(.//em)').extract_first()
            book['price'] = sel.css('div.p-price i::text').extract_first()
            yield book
