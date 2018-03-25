#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://doc.scrapy.org/en/latest/topics/practices.html
https://doc.scrapy.org/en/latest/topics/api.html
https://doc.scrapy.org/en/latest/topics/api.html#module-scrapy.settings
"""


def running_spiders(spiders=[], settings={}, **kwargs):
    from scrapy.settings import Settings
    from scrapy.crawler import CrawlerProcess
    from cells.scrapy import settings as _settings

    spider_settings = Settings()
    spider_settings.setmodule(_settings, priority="command")

    for item in ["SPIDER_MIDDLEWARES", "DOWNLOADER_MIDDLEWARES", "EXTENSIONS", "ITEM_PIPELINES"]:
        spider_settings[item].update(settings.pop(item, {}), priority="project")

    if settings:
        spider_settings.update(settings, priority="project")

    process = CrawlerProcess(spider_settings.copy_to_dict())

    if not isinstance(spiders, list):
        spiders = [spiders]

    for item_spider in spiders:
        process.crawl(item_spider, **kwargs)

    process.start()
