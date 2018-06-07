#!/usr/bin/env python
# -*- coding: utf-8 -*

import logging
import sys
from logging.handlers import RotatingFileHandler
from os.path import join

_FORMATTER = "%(asctime)s [%(name)s] [%(filename)s#L%(lineno)d] %(levelname)s %(message)s"
_MAX_BYTES = 30 * 1024 * 1024  # 30M
_BACKUP_COUNT = 10
_FILE_DELAY = 3


def init_logging(bot_name, path=None, level=logging.INFO, encoding="gbk", format_string=_FORMATTER, **kwargs):
    global _MAX_BYTES, _BACKUP_COUNT, _FILE_DELAY

    if isinstance(level, str):
        level = getattr(logging, level.upper())

    if "maxBytes" in kwargs.keys():
        _MAX_BYTES = kwargs["maxBytes"]

    if "backupCount" in kwargs.keys():
        _BACKUP_COUNT = kwargs["backupCount"]

    if "delay" in kwargs.keys():
        _FILE_DELAY = kwargs["delay"]

    fn = "scrapy-{}.log".format(bot_name)
    if path:
        ph = join(path, fn)
    else:
        ph = fn

    formatter = logging.Formatter(format_string)

    ch = logging.StreamHandler(sys.stdout)
    ch.name = "ext_ch"
    ch.setFormatter(formatter)

    fh = RotatingFileHandler(
        filename=ph,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding=encoding,
        delay=_FILE_DELAY,
    )

    fh.name = "ext_fh"
    fh.level = level
    fh.setFormatter(formatter)

    if fh.name not in [h.name for h in logging.getLogger("scrapy").handlers]:
        logging.getLogger("scrapy").addHandler(fh)

    # if ch.name not in [h.name for h in logging.getLogger().handlers]:
    #     logging.getLogger().addHandler(ch)
