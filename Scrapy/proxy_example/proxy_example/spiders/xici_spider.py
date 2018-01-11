# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


class XiciSpider(scrapy.Spider):
    name = 'xici_spider'
    allowed_domains = ['www.xicidaili.com']
    list_url = 'http://www.xicidaili.com/nn/%s'

    def start_requests(self):
        ip = "127.0.0.1"
        port = "1087"
        scheme = "http"
        url = '%s://httpbin.org/ip' % scheme
        proxy = '%s://%s:%s' % (scheme, ip, port)
        meta = {
            'proxy': proxy,
            'dont_rely': True,
            'download_timeout': 10,

            # 检测字段，传递给check_available方法
            '_proxy_scheme': scheme,
            '_proxy_ip': ip,
        }

        yield Request(url, callback=self.check_available, meta=meta, dont_filter=True)

        for i in range(1, 4):
            yield Request(self.list_url % i)

    def parse(self, response):
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            ip = sel.css('td:nth-child(2)::text').extract_first()
            port = sel.css('td:nth-child(3)::text').extract_first()
            scheme = sel.css('td:nth-child(6)::text').extract_first()

            # 验证代理是否可用
            url = '%s://httpbin.org/ip' % scheme
            proxy = '%s://%s:/%s' % (scheme, ip, port)

            meta = {
                'proxy': proxy,
                'dont_rely': True,
                'download_timeout': 10,

                # 检测字段，传递给check_available方法
                '_proxy_scheme': scheme,
                '_proxy_ip': ip,
            }

            yield Request(url, callback=self.check_available, meta=meta, dont_filter=True)

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        print("proxy_ip  ")
        print(proxy_ip)
        print("\r\r")
        print("response.meta  ")
        print(response.meta)
        print("\r\r")
        print("response.text    ")
        print(response.text)
        print("\r\r")
        print("response    ")
        print(response)

        if proxy_ip == json.loads(response.text)['origin']:
            yield {
                'proxy_scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy']
            }


class TestRandomProxySpider(scrapy.Spider):
    name = "test_random_proxy"

    def start_requests(self):
        for _ in range(5):
            yield Request('http://httpbin.org/ip', dont_filter=True)
            yield Request('https://httpbin.org/ip', dont_filter=True)

    def parse(self, response):
        print(json.loads(response.text))
