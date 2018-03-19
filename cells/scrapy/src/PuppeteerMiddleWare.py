#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DOWNLOADER_MIDDLEWARES = {
    'cells.scrapy.middlewares.PuppeteerMiddleWare': 589/725,
}
"""

from scrapy import signals
from six.moves.urllib_parse import urlencode

from cells.net import add_url_params


class PuppeteerMiddleWare(object):

    def __init__(self, api_url="http://localhost:9081/parse_html"):
        self._puppeteer_api = api_url

        self.remote_keys_key = '_puppeteer_remote_keys'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['PUPPETEER_PARSEHTML_API'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        if not hasattr(spider, 'state'):
            spider.state = {}
        spider.state.setdefault(self.remote_keys_key, {})

    @property
    def _remote_keys(self):
        return self.crawler.spider.state[self.remote_keys_key]

    def process_request(self, request, spider):
        """
        request.meta options:
            is_parse_convert
            parse_html_kws
        """
        if request.meta.get("_puppeteer_processed"):
            # don't process the same request more than once
            return

        request.meta['_puppeteer_processed'] = 1

        if self._puppeteer_api and request.meta.get("parse_html", False):
            params = {"url": request.url}
            params.update(request.meta.get("parse_html_kws", {}))
            params = urlencode(params, doseq=True)

            new_url = add_url_params(self._puppeteer_api, params)
            new_request = request.replace(url=new_url, priority=request.priority + 100)
            return new_request

    def process_response(self, request, response, spider):
        return response
