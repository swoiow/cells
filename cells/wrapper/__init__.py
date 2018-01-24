#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import time


def show_run_time(f):
    @functools.wraps(f)
    def swap(*args, **kwargs):
        print("START TIME：", time.ctime())
        c = time.time()
        print("START TIME：", c)

        f(*args, **kwargs)

        print("LAST TIME：", time.time() - c)
    return swap
