#!/usr/bin/env python
# -*- coding: utf-8 -*

import functools
import inspect
import logging
from logging.handlers import (HTTPHandler, RotatingFileHandler, TimedRotatingFileHandler)
from os.path import curdir, join

_FORMATTER = " %(levelname).1s %(asctime)s [%(name)s:%(filename)s] L%(lineno)d > %(message)s"
_MAX_BYTES = 10 * 1024 * 1024  # 10M
_BACKUP_COUNT = 10
_FILE_DELAY = True
_ENCODING = "utf8"


def add_handle(func):
    @functools.wraps(func)
    def swap(self, *args, **kwargs):
        _func = func(self)

        origin_keys = [v for v in inspect.getfullargspec(_func).args if v not in ["self"]]
        origin_defaults = inspect.getfullargspec(_func).defaults
        origin_params = zip(origin_keys[::-1][:len(origin_defaults)], origin_defaults[::-1])

        # 对外部调用时的 kwargs 参数, 进行预处理
        prepare_params = self.prepare(**kwargs)
        # 与原函数的默认值，和预处理结果进行合并
        mix_params = {**prepare_params, **dict(origin_params)}
        # 根据调用的 keys, 组合参数
        params = {p: mix_params.get(p) for p in origin_keys}

        hd = _func(**params)
        if "level" in prepare_params:
            hd.setLevel(prepare_params["level"])

        if "formatter" in prepare_params:
            hd.setFormatter(prepare_params["formatter"])

        if "hd_name" in prepare_params:
            hd.name = prepare_params["hd_name"]
        else:
            hd.name = "{cls}@{name}: lv{level}".format(
            cls=hd.__class__.__name__,
            name=_func.__name__,
            level=params.get("level", logging.INFO)
        )

        self.inst._call_add_handler(hd)

        # 删除不再需要的对象
        del origin_keys, origin_defaults, origin_params, prepare_params, mix_params

    return swap


class _Handles(object):

    def __init__(self, cls):
        self._inst = self.log_instance = cls

    @property
    def inst(self):
        return self._inst

    def prepare(self, **kwargs):
        maxBytes = max_bytes = kwargs.get("maxBytes", kwargs.get("max_bytes", _MAX_BYTES))
        backupCount = backup_count = kwargs.get("backupCount", kwargs.get("backup_count", _BACKUP_COUNT))
        fileDelay = file_delay = kwargs.get("fileDelay", kwargs.get("file_delay", _FILE_DELAY))

        nm = kwargs.get("filename", kwargs.get("name", self.inst.name))
        ph = kwargs.get("path", curdir)
        name = "{}".format(nm)
        filename = path = join(ph, name)

        level = kwargs.get("level")
        if isinstance(level, str):
            level = getattr(logging, level.upper())

        level = level or self.inst.level
        formatter = kwargs.get("formatter", _FORMATTER)
        formatter = logging.Formatter(formatter)

        return {**kwargs, **locals()}

    @add_handle
    def lgg_RotatingFileHandler(self, **kwargs):
        return RotatingFileHandler

    @add_handle
    def lgg_TimedRotatingFileHandler(self, **kwargs):
        return TimedRotatingFileHandler

    @add_handle
    def lgg_HTTPHandler(self, **kwargs):
        return HTTPHandler

    @add_handle
    def lgg_Console(self, **kwargs):
        return logging.StreamHandler

    @add_handle
    def lgg_KafkaHandler(self, **kwargs):
        from .handles.KafkaHandler import KafkaHandle
        return KafkaHandle

    @add_handle
    def lbk_TimedRotatingFileHandler(self, **kwargs):
        from logbook.handlers import TimedRotatingFileHandler
        return TimedRotatingFileHandler


class InitLogger(logging.Logger):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARN = WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self, name, level=logging.NOTSET):
        """
        Initialize the logger with a name and an optional level.
        """
        logging.Filterer.__init__(self)
        self.name = name
        self.level = logging._checkLevel(level)
        self.parent = None
        self.propagate = True
        self.handlers = []
        self.disabled = False

        self.enable = _Handles(self)

    def _call_add_handler(self, hd):
        if hd.name not in [h.name for h in self.handlers]:
            self.addHandler(hd)
        else:
            print("[WARNING] this handle has existed")
            self.warning("this handle has existed !")
