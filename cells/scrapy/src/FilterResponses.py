#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" https://stackoverflow.com/a/23617802

DOWNLOADER_MIDDLEWARES = {
    'cells.scrapy.middlewares.FilterResponses': 999,
}
"""

import re

from scrapy.exceptions import IgnoreRequest


DEFAULT_TYPE_WHITELIST = (r"text", r"/json", r"/html", r"/xml", r"form", r"rss")


class FilterResponses(object):
    """Limit the HTTP response types that Scrapy downloads."""

    @staticmethod
    def is_valid_response(type_whitelist, content_type_header):
        if not isinstance(content_type_header, str):
            content_type_header = content_type_header.decode()

        content_type_header = content_type_header.lower()

        for type_regex in type_whitelist:
            if re.search(type_regex, content_type_header):
                return True

        return False

    def process_response(self, request, response, spider):
        """
        Only allow HTTP response types that that match the given list of
        filtering regexs
        """

        # to specify on a per-spider basis
        type_whitelist = getattr(spider.settings, "response_type_whitelist", DEFAULT_TYPE_WHITELIST)
        content_type_header = response.headers.get("content-type", None)

        if not content_type_header or not type_whitelist:
            return response

        elif self.is_valid_response(type_whitelist, content_type_header):
            return response

        else:
            msg = "Ignoring request {}, content-type[{}] was not in whitelist".format(response.url, content_type_header)
            spider.logger.info(msg)
            raise IgnoreRequest()
