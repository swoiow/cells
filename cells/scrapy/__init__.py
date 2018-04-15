#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://doc.scrapy.org/en/latest/topics/practices.html
https://doc.scrapy.org/en/latest/topics/api.html
https://doc.scrapy.org/en/latest/topics/api.html#module-scrapy.settings
"""


def running_spiders(spiders=[], settings={}, **kwargs):
    """
    :param spiders:
    :param settings: 传入settings，则合并配置；反之，覆盖配置。
    :param kwargs:
    :return:
    """
    from scrapy.settings import Settings
    from scrapy.crawler import CrawlerProcess
    from cells.scrapy import settings as _settings

    spider_settings = Settings()
    spider_settings.setmodule(_settings)

    for item in ["SPIDER_MIDDLEWARES", "DOWNLOADER_MIDDLEWARES", "EXTENSIONS", "ITEM_PIPELINES"]:
        spider_settings[item].update(settings.pop(item, {}))

        # if (item in spider_settings) and (item in settings):
        #     _old_settings = spider_settings.getdict(item)
        #     _new_settings = settings.pop(item)
        #
        #     merge_settings = {**_old_settings, **_new_settings}
        #     spider_settings.update({item: merge_settings})

    if settings:
        spider_settings.update(settings)

    process = CrawlerProcess(settings=spider_settings)

    if not isinstance(spiders, list):
        spiders = [spiders]

    for item_spider in spiders:
        process.crawl(item_spider, **kwargs)

    process.start()
