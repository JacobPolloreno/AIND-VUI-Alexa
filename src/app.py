#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Utility file for zappa deployment. For some reason Flask blueprints have some
trouble running on AWS Lambda.

When developing, run your app normally with 'index.py' but when you deploy
using Zappa. Make sure the 'zappa_settings.json' file 'app_function' value
is 'src.app.app' NOT 'src.index.app' or 'src.index.create_app'
"""

from src.index import create_app

app = create_app()
