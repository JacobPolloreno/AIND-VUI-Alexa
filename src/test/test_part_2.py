#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

# import pytest
import json
import re
import test.requests as requests
from test.conftest import post
from test.utils import _read_speechassets, _read_facts

schema = _read_speechassets('IntentSchema.json')
intents = json.load(schema)['intents']
utterances = _read_speechassets('SampleUtterances_en_US.txt').readlines()
facts = _read_facts()
facts = {k: v for k, v in facts.items() if 'facts_en_' in k}


def test_utterances_list_getNewYearFactIntent():
    newYearUtterances = [u for u in utterances
                         if 'GetNewYearFactIntent' in utterances]
    assert len(newYearUtterances) >= 15,\
        "should have at least 15 utterances for GetNewYearFactIntent"

    count = 0
    for u in utterances:
        count += len(re.findall('{FACT_YEAR}', u))

    assert count >= 15,\
        "should have at least 15 FACT_YEAR slots"


def test_intentSchema_slots():
    hasYearIntent = False
    slots = None
    for intent in intents:
        if intent['intent'] == 'GetNewYearFactIntent':
            hasYearIntent = True
            try:
                slots = intent['slots']
            except KeyError:
                slots = []

    assert hasYearIntent,\
        "should include GetNewYearFactIntent in IntentSchema.json"

    assert len(slots), "should include a slot"

    hasCorrectSlot = False
    for slot in slots:
        if slot['name'] == 'FACT_YEAR':
            hasCorrectSlot = True

    assert hasCorrectSlot, "should include a slot named FACT_YEAR"


def test_getNewYearFactIntent_with_valid_year(client):
    facts_str = ' '.join([v for k, v in facts.items()])
    years = re.findall('\d{4}', facts_str)

    # Grab invalid year event
    valid_year = json.load(requests.get_new_year_fact_1())
    # Modify the year value in the json dict
    valid_year['request']['intent']['slots']['FACT_YEAR']['value'] = years[0]

    response = post(client, json.dumps(valid_year))

    assert response['response'],\
        "should have a speechlet response"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    assert response['response']['card'],\
        "should have a card response"
