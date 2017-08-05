#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests Part 1 against My History Skill webapp logic
"""

from test.utils import _read_speechassets, _read_facts, has_four_digit_number

UTTERANCES = _read_speechassets('SampleUtterances_en_US.txt').readlines()
UTTERANCES = [u for u in UTTERANCES if 'GetNewFactIntent' in u]
FACTS = _read_facts()
FACTS = {k: v for k, v in FACTS.items() if 'facts_en_' in k}


def test_utterances_list():
    assert len(UTTERANCES) >= 15,\
        "should have at least 15 utterances for GetNewFactIntent"


def test_fact_list_items():
    assert len(FACTS) >= 10,\
        "should have at least 10 facts"

    failed = {}
    for f_k, f_v in FACTS.items():
        if not has_four_digit_number(f_v):
            failed[f_k] = f_v

    assert not failed,\
        "each fact should include a 4-digit year"
