#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser


class ModConfig(object):
    def __init__(self, path):
        self.cfg = ConfigParser()
        self.cfg_path = path

        self.read()

    def read(self):
        self.cfg.read(self.cfg_path)

    def get_value_by_col_key(self, col, key):
        result = self.cfg.get(col, key).strip().split("\n")
        if len(result) == 1:
            return result[0]
        return result
