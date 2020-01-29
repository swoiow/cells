#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" dependencies:
https://hub.docker.com/r/pylab/puppeteer
https://github.com/swoiow/ocr_server/tree/nodejs

DOWNLOADER_MIDDLEWARES = {
    'cells.scrapy.middlewares.PuppeteerMiddleWare': 589/725,
}
"""

from scrapy import signals
from six.moves.urllib_parse import urlencode

from cells.net import add_url_params


class PuppeteerMiddleWare(object):
    """ settings:
            PUPPETEER_API
    """

    def __init__(self, api_url=None):
        self._puppeteer_api = api_url

        self.remote_keys_key = '_puppeteer_remote_keys'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['PUPPETEER_API'])
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
            api_use_post[bool]
            api_ex_kws[dict]: receive extra params for GET
        """

        if request.meta.get("_puppeteer_processed"):
            # don't process the same request more than once
            return

        request.meta['_puppeteer_processed'] = 1

        assert self._puppeteer_api is not None

        origin_url = request.url
        replace_kwargs = {}
        params = request.meta.get("api_ex_kws", {})
        params.update(dict(url=origin_url))

        if request.meta.get("api_use_post"):
            request.headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')

            querystr = urlencode(params, doseq=1)  # Scrapy Example Code => _urlencode(dict.items, request.encoding)
            replace_kwargs.update(dict(
                url=self._puppeteer_api, priority=request.priority + 100,
                method="post", body=querystr
            ))

        else:
            params = urlencode(params, doseq=1)
            redirect_url = add_url_params(self._puppeteer_api, params)

            replace_kwargs.update(dict(url=redirect_url, priority=request.priority + 100))

        request.meta["origin_url"] = origin_url
        new_request = request.replace(**replace_kwargs)

        return new_request

    def process_response(self, request, response, spider):
        new_response = response.replace(url=request.meta.pop("origin_url"))
        return new_response
