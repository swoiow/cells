#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import threading


def TWorker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def t_func(*args, **kwargs):
            """
            :param args:
            :param kwargs:
                    t_name
                    callback
            :return:
            """
            result = func(*args, **kwargs)

            if kwargs.get("callback"):
                return kwargs["callback"](result)
            else:
                rtn = dict(result=True, details="finish")
                return rtn

        # if kwargs.get("t_name", None) in [item.name for item in threading.enumerate()]:
        #     raise RuntimeError("threading is exist")

        t = threading.Thread(target=t_func, args=args, kwargs=kwargs)
        t.setName(kwargs.get("t_name", func.__name__))
        t.setDaemon(True)
        t.start()

        rtn = dict(result=True, details="add")
        return rtn

    return wrapper
