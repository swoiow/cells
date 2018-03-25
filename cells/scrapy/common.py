#!/usr/bin/env python
# -*- coding: utf-8 -*-

import posixpath
import re

import six.moves.urllib.parse as urlparse

WHITE_LIST = ["html", "xhtml", "shtml", "htm", "php", "jsp", "cgi"]
BLACK_LIST = [
    "doc", "docx", "ppt", "pptx", "xls", "xlsx", "pdf", "tif", "zip", "rar", "jpg", "png", "gif", "jpeg", ".swf",
    ".txt", ".img", ".ico", ".css", ".js", ".xml", ".svg", ".json", ".scss"
]


def format_url(uri):
    """fix no scheme url """
    uri = re.sub(r'''[\\"']''', "", uri)
    uri = urlparse.urlparse(uri, scheme="http")
    if uri.scheme in ["http", "https"]:
        # return urlparse.urlunparse(uri)
        return uri.scheme + "://" + uri.netloc + uri.path


def fix_relative_url(uri, path="/"):
    if 'http://' != path[:7] and 'https://' != path[:8]:
        new_uri = urlparse.urljoin(uri, path)

        new_uri_arr = urlparse.urlparse(new_uri)
        new_path = posixpath.normpath(new_uri_arr[2])
        new_uri = urlparse.urlunparse((
            new_uri_arr.scheme, new_uri_arr.netloc, new_path, new_uri_arr.params, new_uri_arr.query,
            new_uri_arr.fragment
        ))

        return new_uri

    elif 'http://' != path[:7] or 'https://' != path[:8]:
        return uri

    return None


def file_or_not(uri, use="white_list", **kwargs):
    uri_arr = urlparse.urlparse(uri)
    end_prefix = uri_arr.path.lower().rsplit(".", 1)

    white_list = kwargs.get("white_list") and kwargs["white_list"] or WHITE_LIST
    black_list = kwargs.get("black_list") and kwargs["black_list"] or BLACK_LIST

    if use == "white_list":
        if end_prefix[-1] in white_list:
            return uri

    elif use == "black_list":
        if not any(map(lambda x: uri.lower().find(x) > -1, black_list)):
            return uri

    else:
        return False


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val and val not in seen:
            yield item
            seen.add(val)
