#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    doc: http://docs.sqlalchemy.org/en/latest/orm/contextual.html
"""

from __future__ import absolute_import

import os

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__all_ = ["engine", "Session", "Base", "MyBase"]

DB_URL = os.environ.get("DATABASE_URI")

if not DB_URL:
    raise Exception("没找到环境变量'DATABASE_URI'的值")

print("-" * 20)
print(DB_URL)
print("=" * 20)

engine = sa.create_engine(DB_URL, convert_unicode=True)
Session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)

Base = declarative_base()


class MyORMBase(object):
    query = Session.query_property()

    def row2dict(self, r):
        return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def _init_more(self, **kwargs):
        for obj in (f for f in self.__class__.__dict__.keys() if not f.startswith("_")):
            if kwargs.get(obj):
                setattr(self, obj, kwargs[obj])

    def __repr__(self):
        return '<%s @%#x>' % (self.__class__.__name__, id(self))
