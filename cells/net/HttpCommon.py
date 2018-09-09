#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict

from ._user_agents import (_browser, _mobile, _spider)


class _AdditionHeader(object):
    @staticmethod
    def add_form_header(header: dict, **kwargs):
        hd = {"Content-Type": "application/x-www-form-urlencoded"}
        header.update(**hd)
        header.update(**kwargs)
        return header

    @staticmethod
    def add_textxml_header(header: dict, **kwargs):
        hd = {"Content-Type": "text/xml; charset=utf-8"}
        header.update(**hd)
        header.update(**kwargs)
        return header

    @staticmethod
    def add_textplain_header(header: dict, **kwargs):
        hd = {"Content-Type": "text/plain; charset=UTF-8"}
        header.update(**hd)
        header.update(**kwargs)
        return header

    @staticmethod
    def add_ajax_header(header: dict, **kwargs):
        hd = {"X-Requested-With": "XMLHttpRequest"}
        header.update(**hd)
        header.update(**kwargs)
        return header

    @staticmethod
    def add_json_header(header: dict, **kwargs):
        hd = {"Content-Type": "application/json; charset=UTF-8"}
        header.update(**hd)
        header.update(**kwargs)
        return header


class _HTTPHeaders(_AdditionHeader):
    TYPE_BOT = _spider
    TYPE_SPIDER = _spider

    TYPE_PC = _browser
    TYPE_BROWSER = _browser

    TYPE_MOBILE = _mobile
    TYPE_PHONE = _mobile

    @property
    def default(self):
        return self.get()

    @property
    def default_browser(self):
        if not hasattr(self, "__default_browser_uas__"):
            setattr(self, "__default_browser_uas__", self.ua_only())

        return self.get(ua=getattr(self, "__default_browser_uas__"))

    @staticmethod
    def ua_only(uas_type=TYPE_BROWSER):
        return random.choice(list(uas_type()))

    def get(self, ua=None):
        if not ua:
            get_ua = self.ua_only()
        else:
            get_ua = ua

        return OrderedDict({
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "no-cache",
            "DNT": "1",
            "User-Agent": get_ua,
        })

    def get_bot(self):
        return OrderedDict({
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": self.ua_only(self.TYPE_SPIDER),
        })

    @staticmethod
    def virtual_ip():
        randint = random.randint
        modify_list = [
            "Via", "CLIENT_IP", "X-Real-Ip", "REMOTE_ADDR", "REMOTE_HOST", "X-Forwarded-For", "X_FORWARDED_FOR",
        ]

        random_ip = lambda: "%s.%s.%s.%s" % (randint(1, 255), randint(0, 255), randint(0, 255), randint(1, 255))
        ip = random_ip()
        headers = {k: ip for k in modify_list}

        return headers


HTTPHeaders = _HTTPHeaders()
