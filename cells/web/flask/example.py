#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, _request_ctx_stack

app = Flask(__name__)
Session = lambda: dict  # TODO: here should call a db session


@app.before_request
def prepare():
    setattr(_request_ctx_stack.top, "Session", Session())


@app.after_request
def set_header(response, *args, **kwargs):
    response.headers.set("Server", "hidden")
    return response


@app.teardown_appcontext
def finish_clean(exception, *args, **kwargs):
    s = getattr(_request_ctx_stack.top, 'Session', None)
    if s:
        s.remove()
