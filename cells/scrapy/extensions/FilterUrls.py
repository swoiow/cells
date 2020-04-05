#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from scrapy.dupefilters import RFPDupeFilter, BaseDupeFilter
from scrapy.utils.project import data_path
from scrapy.utils.request import request_fingerprint


class BLOOMDupeFilter(RFPDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None, initial_capacity=None, error_rate=None, mode=None):
        from .pybloom import ScalableBloomFilter

        super(BLOOMDupeFilter, self).__init__()
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
        from .pybloom import ScalableBloomFilter

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

    # @staticmethod
    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def close(self, reason):
        if self.file:
            with open(self.file, "wb") as wf:
                self.fingerprints.tofile(wf)


class RedisReBloom(BaseDupeFilter):
    """
    Introduction：
        https://oss.redislabs.com/rebloom/

    Dependence:
        docker run -p 6379:6379 --name redis-rebloom redislabs/rebloom:latest
    """

    def __init__(self, rds, port, key, error_rate=0.01, size=5000000):
        import redis

        self.rds = redis.Redis(host=rds, port=port)
        self.key = key

        c = "BF.RESERVE {key} {rate} {size}".format(key=key, rate=error_rate, size=size)

        if not self.rds.keys(self.key):
            self.rds.execute_command(c)

    @classmethod
    def from_settings(cls, settings):
        rds_addr = settings.get('REBLOOM_RDS_HOST')
        rds_port = settings.get('REBLOOM_RDS_PORT', 6379)
        key_ = settings.get('REBLOOM_KEY')
        error_rate_ = settings.get('REBLOOM_ERROR_RATE', 0.01)
        size_ = settings.get('REBLOOM_SIZE', 5000000)

        return cls(rds=rds_addr, port=rds_port, key=key_, error_rate=error_rate_, size=size_)

    def request_seen(self, request):
        fp = request_fingerprint(request)

        c = "BF.ADD {key} {item}".format(key=self.key, item=fp)
        added = self.rds.execute_command(c)
        return not added
