#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import time


def show_run_time(func):
    @functools.wraps(func)
    def swap(*args, **kwargs):
        c = time.time()
        print("START TIME：{} ({})".format(time.ctime(), c))

        func(*args, **kwargs)

        print("LAST TIME：\n", time.time() - c)

    return swap


def catch_err_msg(func):
    import traceback

    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            wrapper.err_msg = func(*args, **kw)
        except Exception as e:
            wrapper.err_msg = e
        finally:
            traceback.print_exc()
            return {"msg": traceback.format_exc()}

    return wrapper
