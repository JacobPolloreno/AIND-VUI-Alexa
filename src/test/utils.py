#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

import os
import io
import re
import six
import yaml

speechAssets_dir = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '../../speechAssets'))

templates_path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                               '../templates.yaml'))


def _read_speechassets(filename):
    with open(speechAssets_dir + '/' + filename, 'r') as f:
        body = f.read()
        return io.StringIO(six.u(body))


def _read_facts():
    with open(templates_path, 'r') as f:
        body = yaml.load(f)

    return body


def has_four_digit_number(fact):
    return len(re.findall(r'(\d{4})', fact)) > 0
