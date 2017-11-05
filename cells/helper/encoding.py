#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    details: https://github.com/Qix-/better-exceptions/blob/master/better_exceptions/core/encoding.py
"""

import sys

PY3 = sys.version_info[0] >= 3

import codecs
import locale

__all__ = ["B", "U", "to_byte", "to_unicode", "to_bool"]

ENCODING = locale.getpreferredencoding()


def to_byte(val):
    unicode_type = str if PY3 else unicode
    if isinstance(val, unicode_type):
        try:
            return val.encode(ENCODING)
        except UnicodeEncodeError:
            if PY3:
                return codecs.escape_decode(val)[0]
            else:
                return val.encode("unicode-escape").decode("string-escape")

    return val


def to_unicode(val):
    if isinstance(val, bytes):
        try:
            return val.decode(ENCODING)
        except UnicodeDecodeError:
            return val.decode("unicode-escape")

    return val


def to_bool(value):
    if str(value).lower() in ("yes", "y", "true", "t", "1", "on"):
        return True
    elif str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "off", "", " ", "none", "[]", "{}"):
        return False
    raise Exception("Invalid value for boolean conversion: " + str(value))


B = lambda x: to_byte(x)
U = lambda x: to_unicode(x)
