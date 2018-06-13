#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict

from ._user_agents import (_browser, _mobile, _spider)


class _UA(object):
    spider = list(_spider())
    browser = list(_browser())
    mobile = list(_mobile())

    TYPE_BOT = "spider"
    TYPE_SPIDER = "spider"
    TYPE_PC = "browser"
    TYPE_BROWSER = "browser"
    TYPE_MOBILE = "mobile"
    TYPE_PHONE = "mobile"

    @staticmethod
    def get(type_=""):
        type_ = getattr(_UA, type_, _UA.browser)
        return random.choice(type_)


class HTTPHeaders(object):
    @property
    def default(self):
        return self.get()

    @staticmethod
    def ua_only(type_=""):
        return _UA.get(type_=type_)

    @staticmethod
    def get(ua=None):
        if not ua:
            get_ua = _UA.get()
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

    @staticmethod
    def get_bot():
        return OrderedDict({
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": _UA.get(_UA.TYPE_SPIDER),
        })

    @staticmethod
    def virtual_ip():
        randint = random.randint
        modify_list = [
            "Via", "CLIENT_IP", "X-Real-Ip", "REMOTE_ADDR", "REMOTE_HOST", "X-Forwarded-For", "X_FORWARDED_FOR"
        ]
        random_ip = lambda: "%s.%s.%s.%s" % (randint(1, 255), randint(0, 255), randint(0, 255), randint(1, 255))
        ip = random_ip()
        headers = {k: ip for k in modify_list}
        return headers


if __name__ == "__main__":
    print(HTTPHeaders.get_bot())
