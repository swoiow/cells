#!/usr/bin/env python
# -*- coding: utf-8 -*

from os import makedirs

from .logger import init_logging


class LoggerExtension(object):
    @classmethod
    def from_crawler(cls, crawler):
        ph = crawler.settings.get("LOG_PATH", "/var/log")
        makedirs(ph, exist_ok=True)

        init_logging(
            bot_name=crawler.settings.get("BOT_NAME", "default"),
            path=ph,
            level=crawler.settings.get("LOG_LEVEL", "INFO"),
            encoding=crawler.settings.get("LOG_ENCODING", "gbk"),
        )

        ext = cls()

        return ext
