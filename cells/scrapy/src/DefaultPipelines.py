#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from os import environ

import sqlalchemy as sa
from celorm.utils import db_read, db_write


class Pipeline(object):
    INNER_TIME = time.time()

    def open_spider(self, spider):
        sa_url = environ["sa_url"]

        self.ENG = sa.create_engine(sa_url, strategy='threadlocal')
        self.INST_BUCKET = []

    def process_item(self, item, spider):
        model = spider.model

        o = model(**item)
        with db_read(self.ENG) as db:
            if db.query(model.id).filter(model.hash == o.hash).count() < 1:
                self.INST_BUCKET.append(o)

        if time.time() > self.INNER_TIME + 60:
            with db_write(self.ENG) as db:
                db.bulk_save_objects(self.INST_BUCKET)

                spider.logger.info(
                    "Heartbeat: %s => %s" % (time.strftime("%Y-%m-%dT%H:%M:%S"), len(self.INST_BUCKET))
                )

            self.INST_BUCKET.clear()
            self.INNER_TIME = time.time()

        return item

    def close_spider(self, spider):
        with db_write(self.ENG) as db:
            db.bulk_save_objects(self.INST_BUCKET)

        self.INST_BUCKET.clear()

        spider.logger.info("close_spider ... 88")
