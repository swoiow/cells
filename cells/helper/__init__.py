#!/usr/bin/env python
# -*- coding: utf-8 -*-


def to_bool(value):
    if str(value).lower() in ("yes", "y", "true", "t", "1", "on"):
        return True
    elif str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "off", "", " ", "none", "[]", "{}"):
        return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))
