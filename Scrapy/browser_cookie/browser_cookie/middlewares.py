# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import browsercookie
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware


class BrowserCookieSpiderMiddleware(CookiesMiddleware):
    def __init__(self, debug=False):
        super().__init__(debug)
        self.load_browser_coockies()

    def load_browser_coockies(self):
        jar = self.jars['chrome']
        chrome_cookiejar = browsercookie.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)

        # jar = self.jars['firefox']
        # firefox_cookiejar = browsercookie.firefox()
        # for cookie in firefox_cookiejar:
        #     jar.set_cookie(cookie)
