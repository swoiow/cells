#!/usr/bin/env python
# -*- coding: utf-8 -*-


def running_spiders(spiders=[], settings={}):
    import scrapy
    from scrapy.crawler import CrawlerProcess

    from cells.scrapy import settings as _settings

    spider_settings = {k: v for k, v in _settings.__dict__.items() if not k.startswith("_")}
    for item in ["JOBDIR", "DUPEFILTER_CLASS"]:
        spider_settings.pop(item)
    spider_settings.update(settings)

    process = CrawlerProcess(spider_settings)

    if scrapy.Spider in spiders.__mro__:
        spiders = [spiders]

    for item_spider in spiders:
        process.crawl(item_spider)

    process.start()
