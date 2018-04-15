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

    def __init__(self, proxy_api="http://localhost:5000/get", max_proxy_retry=10):
        self.proxy_api = proxy_api
        self._max_proxy_retry = max_proxy_retry

    def get_proxy_ip(self):
        resp = requests.get(self.proxy_api)
        return resp.json()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(
            proxy_api=crawler.settings['PROXY_API'],
            max_proxy_retry=crawler.settings.get("MAX_PROXY_RETRY", 10)
        )
        return o

    def process_request(self, request, spider):
        proxy_data = self.get_proxy_ip()
        request.meta['proxy'] = "{protocol}://{addr}".format(**proxy_data)
        logger.info('{} using proxy with [{protocol}]{addr}'.format(request.url, **proxy_data))

    def process_exception(self, request, exception, spider):
        """ refresh proxy in request.meta """
        request.meta['retry_stat'] = request.meta.get("retry_stat", 0) + 1
        request.priority = request.priority - 1

        if request.meta['retry_stat'] < self._max_proxy_retry:
            return request
        else:
            logger.error('Max retry in [{}] '.format(request.url))
            return None
