#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Utils for testing
"""

import os
import io
import json
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


def get_num_included_phrases(results, fact_msgs):
    """
    """

    included_fact_msgs = []

    for r in results:
        for f_k, f_v in fact_msgs.items():
            if f_v in r:
                included_fact_msgs.append(f_k)

    return len(set(included_fact_msgs)) > 1


def has_year_intent_schema():
    intents = json.load(_read_speechassets('IntentSchema.json'))['intents']
    has_year_intent_schema = False
    for intent in intents:
        if intent['intent'] == 'GetNewYearFactIntent':
            has_year_intent_schema = True

    return has_year_intent_schema
