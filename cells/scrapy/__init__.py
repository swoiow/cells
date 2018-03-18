#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://doc.scrapy.org/en/latest/topics/practices.html
https://doc.scrapy.org/en/latest/topics/api.html
https://doc.scrapy.org/en/latest/topics/api.html#module-scrapy.settings
"""


def running_spiders(spiders=[], settings={}):
    import scrapy
    from scrapy.settings import Settings
    from scrapy.crawler import CrawlerProcess
    from cells.scrapy import settings as _settings

    spider_settings = Settings()
    spider_settings.setmodule(_settings, priority="project")

    for item in ["JOBDIR", "DUPEFILTER_CLASS"]:
        spider_settings.pop(item)

    for item in ["SPIDER_MIDDLEWARES", "DOWNLOADER_MIDDLEWARES", "EXTENSIONS", "ITEM_PIPELINES"]:
        spider_settings[item].update(settings.pop(item, {}), priority="cmdline")

    if settings:
        spider_settings.update(settings, priority="cmdline")

    process = CrawlerProcess(spider_settings.copy_to_dict())

    if scrapy.Spider in spiders.__mro__:
        spiders = [spiders]

    for item_spider in spiders:
        process.crawl(item_spider)

    process.start()
