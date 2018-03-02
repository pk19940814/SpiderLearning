# -*- coding: utf-8 -*-
import scrapy
from ..items import JobInfo
from scrapy.linkextractors import LinkExtractor


class Csq51Spider(scrapy.Spider):
    name = 'csq51'
    allowed_domains = ['51job.com']
    BASE_URL = 'http://search.51job.com/list/020000,000000,0000,00,9,99,%%2B,2,%s.html?lang=c&stype=1&postchannel=0000'
    '&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&'
    'confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    STEP = 50
    LIMIT = 200
    index = 1
    start_urls = [BASE_URL % str(index)]

    # 工作列表页面的解析函数
    def parse(self, response):
        le = LinkExtractor(restrict_css='p.t1  span')

        # yield scrapy.Request(le.extract_links(response)[0].url, callback=self.parse_job)

        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_job)

        if self.index * self.STEP < self.LIMIT:
            self.index = self.index + 1
            next_url = self.BASE_URL % self.index
            yield scrapy.Request(next_url, callback=self.parse)

    # 工作详情页面的解析函数
    def parse_job(self, response):
        job_info = JobInfo()

        sel = response.css('div.tHeader.tHjob')
        job_info['name'] = sel.css('div.cn h1::text').extract_first()
        job_info['area'] = sel.css('div.cn span::text').extract_first()
        job_info['salary'] = sel.css('div.cn strong::text').extract_first()
        job_info['corp_name'] = sel.css('div.cn p a::text').extract_first()
        job_info['description'] = sel.xpath('.//div[@class="cn"]/p[@class="msg ltype"]/text()') \
            .extract_first().replace(' ', '').replace('\t', '')

        sel = response.css('div.tBorderTop_box.bt')
        job_info['job_restrict'] = sel.css('div.t1 span.sp4::text').extract()
        job_info['welfare'] = sel.css('p.t2 span::text').extract()
        print(job_info)
        yield job_info
