#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    document online: http://sqlalchemy-migrate.readthedocs.io/en/latest/api.html
        ?highlight=update_db_from_model
    document: migrate.versioning.api

    使用方法：
        1. 没有创建过数据库的情况下，补充:
            SQLALCHEMY_DATABASE_URI
            SQLALCHEMY_MIGRATE_REPO
        1.2 执行 `DataBaseCLI.create()` 进行创建。

        2. import 相关的表，如:
                from models.sys import User
                from models.url import ShortUrl
                from models.blog import (Post,Tags)

           import 基础的base:
                from models import dbutils

        3. 执行合并。
            DataBaseCLI.migrate(dbutils.Base)

        4. 进行降级。
            DataBaseCLI.downgrade(版本号)

        5. 只测试不执行写入。
            DataBaseCLI.manage_test()
"""

import os
import types

from migrate.versioning import api

PROJECT_NAME = "default"
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///.aa.db")
SQLALCHEMY_MIGRATE_REPO = ".db_repo"


class DataBaseCLI(object):
    repository_version = os.path.exists(SQLALCHEMY_MIGRATE_REPO) \
                         and api.version(SQLALCHEMY_MIGRATE_REPO) \
                         or None

    @staticmethod
    def create():
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, PROJECT_NAME)
            api.version_control(
                SQLALCHEMY_DATABASE_URI,
                SQLALCHEMY_MIGRATE_REPO
            )
        else:
            api.version_control(
                SQLALCHEMY_DATABASE_URI,
                SQLALCHEMY_MIGRATE_REPO,
                DataBaseCLI.repository_version
            )

    @staticmethod
    def migrate(model):
        REPO = SQLALCHEMY_MIGRATE_REPO

        migration = REPO + "/versions/%03d_migration.py" % (DataBaseCLI().ver + 1)
        tmp_module = types.ModuleType("old_model")
        old_model = api.create_model(SQLALCHEMY_DATABASE_URI, REPO)
        exec(old_model, tmp_module.__dict__)

        script = api.make_update_script_for_model(
            SQLALCHEMY_DATABASE_URI,
            REPO,
            tmp_module.meta,
            model.metadata
        )

        open(migration, "wt").write(script)
        api.upgrade(SQLALCHEMY_DATABASE_URI, REPO)
        print("New migration saved as " + migration)
        print("Current database version: " + str(DataBaseCLI().ver))

    @staticmethod
    def upgrade():
        api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        print("Current database version: " + str(DataBaseCLI().ver))

    @staticmethod
    def update_db_from_model(model, **opts):
        api.update_db_from_model(
            SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO,
            model,
            **opts
        )

        print("Current database version: " + str(DataBaseCLI().ver))

    @staticmethod
    def downgrade(version=None):
        if not version:
            v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            version = v - 1

        if version > DataBaseCLI.repository_version:
            raise ValueError("input version > current version")

        api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, version)
        print("Current database version: " + str(DataBaseCLI().ver))

    @property
    def ver(self):
        return self.version()

    @staticmethod
    def version(by_db=True):
        if by_db:
            return DataBaseCLI._version_by_db()
        else:
            return DataBaseCLI.repository_version

    @staticmethod
    def _version_by_db():
        v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        return v

    @staticmethod
    def generate_sql_file(database_type):
        # 待完善
        api.script_sql(
            database_type,
            description="generate",
            repository=SQLALCHEMY_MIGRATE_REPO
        )

    @staticmethod
    def manage_test():
        api.test(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)


def merge_base(*args):
    from sqlalchemy import MetaData

    combined_meta_data = MetaData()

    for declarative_base in args:
        for (table_name, table) in declarative_base.metadata.tables.items():
            combined_meta_data._add_table(table_name, table.schema, table)

    return combined_meta_data


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    DataBaseCLI.create()
    # import some orm, such as:
    # from model import Post
    from cells.db import dbutils

    DataBaseCLI.migrate(dbutils.Base)
