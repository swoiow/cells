#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Drop:
     https://doc.scrapy.org/en/1.1/topics/settings.html?highlight=context#downloader-client-tls-method
Usage:
    DOWNLOADER_CLIENTCONTEXTFACTORY = 'spider.contexts.CustomContextFactory'
"""

from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory


class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """

    def __init__(self):
        # Use SSLv23_METHOD so we can use protocol negotiation
        self.method = SSL.SSLv23_METHOD
