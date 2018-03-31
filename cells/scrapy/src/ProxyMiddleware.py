#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
DOWNLOADER_MIDDLEWARES = {
    'cells.scrapy.middlewares.ProxyMiddleware': 749,
}
"""

import logging

import requests

logger = logging.getLogger(__name__)


class ProxyMiddleware(object):

    def __init__(self, proxy_api="http://localhost:5000/get"):
        self.proxy_api = proxy_api

    def get_proxy_ip(self):
        resp = requests.get(self.proxy_api)
        return resp.json()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['PROXY_API'])
        return o

    def process_request(self, request, spider):
        proxy_data = self.get_proxy_ip()
        request.meta['proxy'] = "{protocol}://{addr}".format(**proxy_data)
        logger.debug('{} using proxy with [{protocol}]{addr}'.format(request.url, **proxy_data))

    def process_exception(self, request, exception, spider):
        """ refresh proxy in request.meta """
        proxy_data = self.get_proxy_ip()
        request.meta['proxy'] = "{protocol}://{addr}".format(**proxy_data)
        request.meta['retry_time'] = request.meta.get("retry_time", 0) + 1

        if request.meta['retry_time'] < 10:
            return request
        else:
            return None
