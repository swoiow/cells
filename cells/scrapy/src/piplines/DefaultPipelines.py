#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from os import environ

import sqlalchemy as sa
from celorm.utils import db_read, db_write

__name__ = 'DefaultPipelines'


class BatchSave(object):

    def __init_subclass__(cls, **kwargs):
        cls.INNER_TIME = time.time()
        cls.INST_BUCKET = []

        cls.ENGINE = cls._create_connect()

    @staticmethod
    def _create_connect():
        sa_url = environ["sa_url"]
        return sa.create_engine(sa_url, strategy='threadlocal')

    def push(self, model, item):
        with db_read(self.ENGINE) as db:
            if db.query(model.id).filter(model.hash == item.hash).count() < 1:
                self.INST_BUCKET.append(item)

    def commit(self):
        if time.time() > self.INNER_TIME + 60:
            with db_write(self.ENGINE) as db:
                db.bulk_save_objects(self.INST_BUCKET)

            return True
        return False

    def clear(self):
        self.INST_BUCKET.clear()

    def update_counter(self):
        self.INNER_TIME = time.time()


class Pipeline(BatchSave):

    def open_spider(self, spider):
        spider.logger.info(f"{__name__} is initialized.")

    def process_item(self, item, spider):
        model = spider.model

        o = model(**item)
        self.push(model, item=o)

        if self.commit():
            spider.logger.info(f"Heartbeat: {time.strftime('%Y-%m-%dT%H:%M:%S')} => {len(self.INST_BUCKET)}")

            self.clear()
            self.update_counter()

        return item

    def close_spider(self, spider):
        self.commit()
        self.clear()

        spider.logger.info("close_spider ... 88")
