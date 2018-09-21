#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from celorm import utils as dbutils
    from celorm.helper import *

except ImportError:
    from cells.helper.colorprint import ColorPrint as _

    message = "this package has been merged into celorm. \n" \
              "if you want to use this package, please install celorm with: \n" \
              "pip install https://github.com/swoiow/celorm/archive/master.zip \n"

    _.print_warn(message)
