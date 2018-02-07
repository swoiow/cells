#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import time


def show_run_time(f):
    @functools.wraps(f)
    def swap(*args, **kwargs):
        c = time.time()
        print("START TIME：{} ({})".format(time.ctime(), c))

        f(*args, **kwargs)

        print("LAST TIME：\n", time.time() - c)

    return swap
