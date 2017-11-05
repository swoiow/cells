#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import os
from base64 import urlsafe_b64encode


def generate_csrf_token(sessionObj):
    if "_csrf_token" not in sessionObj:
        sessionObj["_csrf_token"] = urlsafe_b64encode(os.urandom(12))
    return sessionObj["_csrf_token"]


def datetime_format(dt, fmt="%Y-%m-%d %H:%M:%S", to_local=True):
    if not dt: return

    if to_local:
        new_dt = dt + datetime.timedelta(hours=8)
        return new_dt.strftime(fmt)
    return dt.strftime(fmt)


del os
