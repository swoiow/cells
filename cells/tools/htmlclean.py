#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import partial

try:
    import bleach
    from lxml.html import defs

except ImportError as e:
    from colorama import Fore

    print(Fore.RED + e.msg)
    exit(127)

__all__ = ["HtmlClean"]

cfg = {
    "tags": defs.block_tags,
    "attrs": {
        "*": defs.safe_attrs,
        "a": ["href", "title"],
        "acronym": ["title"],
        "abbr": ["title"],
        "img": ["alt"],
        "applet": ["code", "object"],
        "embed": ["src"],
        "iframe": ["src"],
        "layer": ["src"],
        "link": ["href"],
        "script": ["src"],
    },
    "protocols": ["http", "https", "mailto", "sss"],
    "style": [
        "color", "font-size", "font-style", "font-weight", "margin", "margin-left", "text-align",
        "text-decoration",
    ],
}

HtmlClean = partial(
    bleach.clean,
    tags=cfg["tags"],
    attributes=cfg["attrs"],
    protocols=cfg["protocols"],
)
