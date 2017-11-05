#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bleach
from functools import partial
from blogsettings import cfg

__all__ = ["HtmlClean"]

HtmlClean = partial(
    bleach.clean,
    tags=cfg["_bleach"]["tags"],
    attributes=cfg["_bleach"]["attrs"],
    protocols=cfg["_bleach"]["protocols"],
)
