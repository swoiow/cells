#!/usr/bin/env python
# -*- coding: utf-8 -*-


def generate_sql_exec(table_name, item):
    columns = ", ".join(item.keys())
    placeholders = ", ".join(["%s"] * len(item))
    sql_exec = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, placeholders)

    return sql_exec
