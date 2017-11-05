#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six.moves.urllib.parse as urllib


def get_argument(request, name, default="", strip=True):
    if strip:
        return request.values.get(name, default).strip()
    return request.values.get(name, default)


def get_arguments(request, strip=True):
    if strip:
        vals = dict()
        for k, v in request.values.items():
            if isinstance(v, (str, unicode, bytes)):
                new_v = char_transform(v, to_str=True).strip()
                vals[k] = char_transform(new_v)
            else:
                vals[k] = v
        return vals

    return dict(request.values)


def setup_page(request, flag="page"):
    page_number = request.values.get(flag, 1)
    page_number = 1 if (page_number and int(page_number) < 1) else int(page_number)

    f = lambda d: "?" + urllib.urlencode(d)
    args = {k: v for k, v in request.values.items()}
    # prev_pn = 1 if (page_number < 2) else (page_number - 1)
    # next_pn = page_number + 1

    if page_number < 5:
        batch = [(i, f(dict(args, **{flag: i}))) for i in range(1, 10)]
    else:
        batch = [(i, f(dict(args, **{flag: i}))) for i in range(page_number - 4, page_number + 5)]

    return page_number, batch
