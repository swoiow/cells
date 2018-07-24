#!/usr/bin/env python
# -*- coding: utf-8 -*

import datetime
import logging


class _FmtLogbook2Logging(logging.Filter):
    """ convert logbook format -> logging format """

    def __init__(self):
        super(_FmtLogbook2Logging, self).__init__(name=self.__class__.__name__)

    def filter(self, record):
        if not hasattr(record, "msg"):
            record.msg = record.message

        return record


class _FmtRecord2ES(logging.Filter):

    def __init__(self):
        super(_FmtRecord2ES, self).__init__(name=self.__class__.__name__)

    def filter(self, record):
        if isinstance(record.msg, dict):
            if "@timestamp" not in record.msg:
                record.msg.update({"@timestamp": datetime.datetime.utcnow()})
        else:
            print("[警告] 由于 message 不是 dict 类型, 转换.")
            _dict = dict(message=record.msg)
            record.msg = _dict
            return self.filter(record)

        return record


FmtLogbook2Logging = _FmtLogbook2Logging()
FmtRecord2ES = _FmtRecord2ES()
