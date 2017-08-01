#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

from test.utils import _read_speechassets, _read_facts, has_four_digit_number

utterances = _read_speechassets('SampleUtterances_en_US.txt').readlines()
utterances = [u for u in utterances if 'GetNewFactIntent' in utterances]
facts = _read_facts()
facts = {k: v for k, v in facts.items() if 'facts_en_' in k}


def test_utterances_list():
    assert len(utterances) >= 15,\
        "should have at least 15 utterances for GetNewFactIntent"


def test_fact_list_items():
    assert len(facts) >= 10,\
        "should have at least 10 facts"

    failed = {}
    for k, v in facts.items():
        if not has_four_digit_number(v):
            failed[k] = v

    assert len(failed) == 0,\
        "each fact should include a 4-digit year"
