#!/usr/bin/env python
# -*- coding: utf-8 -*-

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
}

# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {}

# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "cells.scrapy.middlewares.RandomUserAgentMiddleware": 499,
}

# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {}

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # cells.scrapy.piplines.MariaDBPipeline: 0,
    # cells.scrapy.piplines.PostgreSqlPipeline: 0,
    # cells.scrapy.piplines.MongoDBPipeline: 0,
}

# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = False
# AUTOTHROTTLE_START_DELAY = 1
# AUTOTHROTTLE_MAX_DELAY = 30
# AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0

# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# See https://doc.scrapy.org/en/latest/topics/settings.html#dnscache-enabled
DNS_TIMEOUT = 3

#
# JOBDIR = ".scrapy_jobdir"

LOG_LEVEL = "INFO"
# LOG_FILE = "{}.log".format(BOT_NAME)
LOG_ENCODING = "gbk"
MEMUSAGE_LIMIT_MB = 512 * 6
# DUPEFILTER_CLASS = "cells.scrapy.extensions.BLOOMDupeFilter"

#
# DEPTH_LIMIT = 2
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"
