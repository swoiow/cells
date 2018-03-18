#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.project import data_path
from scrapy.utils.request import request_fingerprint

from .pybloom import ScalableBloomFilter


class BLOOMDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None, initial_capacity=None, error_rate=None, mode=None):
        self.file = None
        self.fingerprints = None

        if path:
            self.file = os.path.join(path, ".BloomFilter.dmp")

            if os.path.exists(self.file):
                with open(self.file, "rb") as rf:
                    self.fingerprints = ScalableBloomFilter.fromfile(rf)

        if not self.fingerprints:
            self.fingerprints = ScalableBloomFilter(initial_capacity, error_rate, mode)

    @classmethod
    def from_settings(cls, settings, **kwargs):
        p = settings.get("BLOOMFILTER_PATH", data_path("."))
        ic = settings.get("BLOOMFILTER_SIZE", 5000000)
        ert = settings.get("BLOOMFILTER_ERROR_RATE", 0.001)
        mode = settings.get("BLOOMFILTER_MODE", ScalableBloomFilter.SMALL_SET_GROWTH)

        return cls(path=p, initial_capacity=ic, error_rate=ert, mode=mode)

    def request_seen(self, request):
        # do something or filter rule with request.url
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)

    @staticmethod
    def request_fingerprint(request):
        return request_fingerprint(request)

    def close(self, reason):
        if self.file:
            with open(self.file, "wb") as wf:
                self.fingerprints.tofile(wf)
