#!/usr/bin/env python
# -*- coding: utf-8 -*-

import difflib
import posixpath
import re

import six.moves.urllib.parse as urlparse


_doc_file_list = ["txt", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "pdf", ]
_zip_file_list = ["zip", "rar", "7z", "tar", "tar.bz", "tar.gz", "xz"]
_img_file_list = ["tif", "jpg", "png", "gif", "jpeg", "swf", ]
_web_file_list = ["img", "ico", "css", "js", "xml", "svg", "json", "scss"]

WHITE_LIST = ["html", "xhtml", "shtml", "htm", "php", "jsp", "cgi"]
BLACK_LIST = _doc_file_list + _zip_file_list + _img_file_list + _web_file_list

_rule = "^.*\.(?:{})+.*$"
DEFAULT_RULE = re.compile(_rule.format("|".join(_web_file_list + _img_file_list)), re.IGNORECASE | re.DOTALL)


def format_url(uri):
    """ [deprecated] fix no scheme url """

    uri = re.sub(r'''[\\"']''', "", uri)
    uri = urlparse.urlparse(uri, scheme="http")
    if uri.scheme in ["http", "https"]:
        # return urlparse.urlunparse(uri)
        return uri.scheme + "://" + uri.netloc + uri.path


def fix_scheme(uri: str, default_scheme="http"):
    """ fix url without scheme """
    uri_obj = urlparse.urlparse(uri)
    if not uri_obj.scheme:
        _uri = "//" + uri
        if _uri[:4] == "////" or _uri[:3] != "///":
            uri_obj = urlparse.urlparse(_uri, scheme=default_scheme)
            return uri_obj.geturl()

    return uri


def fix_relative_url(uri, path, debug=False):
    """
        print(fix_relative_url('http://localhost.com', 'http://localhost.com/aa'))
        print(fix_relative_url('http://localhost.com', '//localhost.com/bb'))
        print(fix_relative_url('http://localhost.com', 'www.localhost.com'))
        print(fix_relative_url("http://localhost.com", "sub1.sub2.localhost.cn/this-is-a-longer-post-title.html"))

        print("-" * 3)
        print(fix_relative_url('http://localhost.com', '/phA/phB'))
        print(fix_relative_url('http://localhost.com', './phA/phB'))
        print("-" * 3)
        print(fix_relative_url('http://localhost.com/phA', '../phA/a.jpg'))
        print(fix_relative_url('http://localhost.com/phA/phB/', '../phC/phD'))
        print("-" * 3)
        print(fix_relative_url('http://domainA.com', 'http://www.domainB.com'))
        print(fix_relative_url('http://domainA.com', 'www.domainB.com/phA'))
        print(fix_relative_url('http://domainA.com', 'phA'))
        print(fix_relative_url('http://domainA.com', 'java'))
    """

    if path.lower().startswith("javascript:"):
        return None

    elif (not path.startswith("/")) and (not path.startswith(".")):
        if debug:
            print(f"[W] => fix_relative_url: failed with `{uri}` & `{path}`")

        len_uri, len_path = len(uri), len(path)
        weights = len_path > len_uri and 1 + len_path // len_uri or 0

        seq = difflib.SequenceMatcher(None, uri, path[:len_uri + weights])
        if seq.ratio() > 0.5:
            return fix_scheme(path)
        else:
            return urlparse.urljoin(uri, path)

    elif path.startswith("//"):
        return fix_scheme(path)

    new_url = urlparse.urljoin(uri, path)

    new_url_array = urlparse.urlparse(new_url)
    new_path = posixpath.normpath(new_url_array[2])
    new_url = urlparse.urlunparse((
        new_url_array.scheme,
        new_url_array.netloc,
        new_path,
        new_url_array.params,
        new_url_array.query,
        new_url_array.fragment
    ))

    return new_url


def file_or_not(uri, rule="white_list", **kwargs):
    """  判断 uri 是否满足 rule 条件, 满足则返回 True """

    uri_arr = urlparse.urlparse(uri)
    end_prefix = uri_arr.path.lower().rsplit(".", 1)

    white_list = "white_list" in kwargs and kwargs["white_list"] or WHITE_LIST
    black_list = "black_list" in kwargs and kwargs["black_list"] or BLACK_LIST

    if "use" in kwargs:
        rule = kwargs["use"]

    if rule == "white_list":
        return end_prefix[-1] in white_list

    elif rule == "black_list":
        return any(list(map(lambda x: uri.lower().find(x) > -1, black_list)))

    else:
        return None


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val and val not in seen:
            yield item
            seen.add(val)

if __name__ == '__main__':
    print(fix_relative_url('http://localhost.com', 'http://localhost.com/aa'))
    print(fix_relative_url('http://localhost.com', '//localhost.com/bb'))
    print(fix_relative_url('http://localhost.com', 'www.localhost.com'))
    print(fix_relative_url("http://localhost.com", "sub1.sub2.localhost.cn/this-is-a-longer-post-title.html"))

    print("-" * 3)
    print(fix_relative_url('http://localhost.com', '/phA/phB'))
    print(fix_relative_url('http://localhost.com', './phA/phB'))
    print("-" * 3)
    print(fix_relative_url('http://localhost.com/phA', '../phA/a.jpg'))
    print(fix_relative_url('http://localhost.com/phA/phB/', '../phC/phD'))
    print("-" * 3)
    print(fix_relative_url('http://domainA.com', 'http://www.domainB.com'))
    print(fix_relative_url('http://domainA.com', 'www.domainB.com/phA'))
    print(fix_relative_url('http://domainA.com', 'phA'))
    print(fix_relative_url('http://domainA.com', 'java'))