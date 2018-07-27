#!/usr/bin/env python
# -*- coding: utf-8 -*

import datetime
import logging

import msgpack
from kafka import KafkaProducer


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


class KafkaHandle(logging.NullHandler):
    def __init__(
            self, kafka_brokers, topic_map,
            acks="all", retries=5, level=logging.NOTSET,
    ):
        super(KafkaHandle, self).__init__()

        self._kafka_producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            acks=acks,
            retries=retries,
            value_serializer=lambda m: msgpack.dumps(m, default=encode_datetime, use_bin_type=True),
        )

        self.topic_map = topic_map
        self.topic_map["warning"] = self.topic_map["warn"]  # [NOTICE] logging 里面弃用了warn

    @property
    def kafka_server(self):
        return self._kafka_producer

    def handle(self, record):
        self.filter(record)
        self.emit(record)

    def emit(self, record):
        kafka_topic = self.topic_map[record.levelname.lower()]
        self.kafka_server.send(kafka_topic, record.msg)

    def __del__(self):
        self.kafka_server.flush(30)
