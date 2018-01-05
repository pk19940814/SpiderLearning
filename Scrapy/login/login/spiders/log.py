# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.log import logger
import json
from PIL import Image
from io import BytesIO
import pytesseract
import requests
import base64
from pprint import pprint


class LogSpider(scrapy.Spider):
    name = 'log'
    allowed_domains = ['webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    def parse(self, response):
        # 解析登录后下载的页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        dict_return = dict(zip(keys, values))
        yield dict_return

    # 登录
    login_url = 'http://example.webscraping.com/places/default/user/login'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        fd = {'email': '362519489@qq.com', 'password': 'pk19940814KOM'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    def parse_login(self, response):
        if 'Welcome' in response.text:
            yield from super().start_requests()


# 验证码登录用demo
class CaptchaLoginSpider(scrapy.Spider):
    name = "login_captcha"
    start_urls = ["http:XXX.com/"]

    def parse(self, response):
        pass

    # X网站的登录页面url
    login_url = "http://XXX.com/login"
    user = "pk@qq.com"
    password = "123456"

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        # 既是登录页面解析函数，也是下载验证码图片的相应处理函数
        # 如果response.meta['login_response']存在，当前response为验证码的相应，否则为登录页面的相应
        login_response = response.meta.get('login_response')

        if not login_response:
            # 此时response为登录页面的相应，从中提取验证码图片的url，下载验证码图片
            captcha_url = response.css('label.field.prepend-icon img::attr(src)').extract_first()
            captcha_url = response.urljoin(captcha_url)
            # 构造request时，将当前response保存到meta字典中
            yield Request(captcha_url, callback=self.login, meta={'login_response': response}, dont_filter=True)

        else:
            # 此时response为验证码图片的相应,response.body是图片二进制数据
            # login_response为登录页面的相应，用其构造表单请求并发送
            formdata = {
                'email': self.user,
                'pass': self.password,
                # 使用OCR识别
                'code': self.get_captcha_by_OCR(response.body),
            }
            yield FormRequest.from_response(login_response, callback=self.parse_login, formdata=formdata,
                                            dont_filter=True)

    def parse_login(self, response):
        # 根据相应结果判断是否登录成功
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('登录成功:-)')
            return super().start_requests()

        logger.info("登录失败:-(，重新登录...")
        return self.start_requests()

    def get_captcha_by_OCR(self, data):
        # OCR识别
        img = Image.open(BytesIO(data))
        img = img.convert('L')
        captcha = pytesseract.image_to_string(img)
        img.close()

        return captcha

    def get_captcha_by_network(self, data):
        url = "http://ali-checkcode.showapi.com/checkcode"
        appcode = 'f23cca37f287418a90e2f922649273c4'
        form = {}
        form['convert_to_jpg'] = '0'
        form['img_base64'] = base64.b64encode(data)
        form['typeId'] = '3040'

        headers = {'Authorization': 'APPCODE' + appcode}
        response = requests.post(url, headers=headers, data=form)
        res = response.json()
        if res['showapi_res_code'] == 0:
            return res['showapi_res_bode']['Result']

        return ''

    def get_captcha_by_user(self, data):
        # 人工识别
        img = Image.open(BytesIO(data))
        img.show()
        captcha = input('请输入验证码:')
        img.close()
        return captcha
