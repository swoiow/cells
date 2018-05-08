#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    doc: http://docs.sqlalchemy.org/en/latest/orm/contextual.html
"""

from __future__ import absolute_import

import os
import sys
import traceback
from contextlib import contextmanager
from datetime import datetime

from six.moves import cPickle
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

__all_ = ["engine", "Session", "Base", "MyBase"]


@contextmanager
def db_write(engine=None):
    """Provide a transactional scope around a series of operations."""

    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)
    # Session = scoped_session(
    #     sessionmaker(bind=engine, autocommit=False, autoflush=False)
    # )

    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        traceback.print_exc()
        f_locals = sys.exc_info()[2].tb_next.tb_frame.f_locals

        _v = {k: v for k, v in f_locals.items() if isinstance(v, (str, bytes, dict, list, tuple))}
        _f = "session_{}.dmp".format(datetime.now().strftime("%Y%m%d%H%M%S_%f"))
        _p = os.path.join(os.getcwd(), _f)
        with open(_p, "wb") as wf:
            cPickle.dump(obj=_v, file=wf)
            print("Error and export dump in => {}".format(_p))

    finally:
        session.close()


@contextmanager
def db_read(engine=None):
    engine = engine or os.environ.get("DATABASE_URI")
    session = Session(bind=engine)

    try:
        yield session
    finally:
        session.close()


Base = declarative_base()


class MyORMBase(object):
    # query = Session.query_property()

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
