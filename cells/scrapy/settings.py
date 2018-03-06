#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = "scrapy"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133"

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
}

# AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0

#
JOBDIR = ".scrapy"

LOG_LEVEL = "INFO"
LOG_FILE = "{}.log".format(BOT_NAME)
LOG_ENCODING = "gbk"
MEMUSAGE_LIMIT_MB = 128
DUPEFILTER_CLASS = "cells.scrapy.BLOOMDupeFilter"

#
DEPTH_PRIORITY = 3
SCHEDULER_DISK_QUEUE = "scrapy.squeue.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeue.FifoMemoryQueue"
