#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bottle import run, debug
from apps.common import blog

os.chdir(os.path.dirname(__file__))

debug(True)
run(blog, reloader=True, host='localhost', port=8080)
#run(blog, server='tornado', reloader=True, host='localhost', port=8080)
