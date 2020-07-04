#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DOWNLOADER_MIDDLEWARES = {
    'cells.scrapy.middlewares.RandomUserAgentMiddleware': 300,
}
"""

from cells.net.HttpCommon import HTTPHeaders
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = HTTPHeaders.ua_only()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)
