#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests Part 2 against My History Skill webapp logic
"""

import json
import re
import test.requests as requests
from test.conftest import post
from test.utils import _read_speechassets, _read_facts

SCHEMA = _read_speechassets('IntentSchema.json')
INTENTS = json.load(SCHEMA)['intents']
UTTERANCES = _read_speechassets('SampleUtterances_en_US.txt').readlines()
FACTS = _read_facts()
FACTS = {k: v for k, v in FACTS.items() if 'facts_en_' in k}

RESULTS = []


def test_utterances_list_getnewyearfactintent():
    new_year_utterances = [u for u in UTTERANCES
                           if 'GetNewYearFactIntent' in u]
    assert len(new_year_utterances) >= 15,\
        "should have at least 15 utterances for GetNewYearFactIntent"

    count = 0
    for utt in UTTERANCES:
        count += len(re.findall('{FACT_YEAR}', utt))

    assert count >= 15,\
        "should have at least 15 FACT_YEAR slots"


def test_intent_schema_slots():
    has_year_intent = False
    slots = None
    for intent in INTENTS:
        if intent['intent'] == 'GetNewYearFactIntent':
            has_year_intent = True
            try:
                slots = intent['slots']
            except KeyError:
                slots = []

    assert has_year_intent,\
        "should include GetNewYearFactIntent in IntentSchema.json"

    assert slots, "should include a slot"

    has_corrrect_slot = False
    for slot in slots:
        if slot['name'] == 'FACT_YEAR':
            has_corrrect_slot = True

    assert has_corrrect_slot, "should include a slot named FACT_YEAR"


def test_getnewyearfactintent_valid_year(client):
    facts_str = ' '.join([v for k, v in FACTS.items()])
    years = re.findall(r'\d{4}', facts_str)

    if years:
        # Grab invalid year(9999) event
        event = json.load(requests.get_new_year_fact())
        # Modify the year value in the json dict
        event['request']['intent']['slots']['FACT_YEAR']['value'] = years[0]

        response = post(client, json.dumps(event))
    else:
        response = post(client, requests.get_new_year_fact())

    assert response['response'],\
        "should have a speechlet response"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    assert response['response']['card'],\
        "should have a card response"

    assert years[0] in response['response']['outputSpeech']['text'],\
        "should have year in the spoken response"


def test_getnewyearfactintent_non_matching_year_1(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should receive response"

    RESULTS.append(response['response']['outputSpeech']['text'])


def test_getnewyearfactintent_non_matching_year_2(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should receive response"

    RESULTS.append(response['response']['outputSpeech']['text'])


def test_getnewyearfactintent_non_matching_year_3(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should receive response"

    RESULTS.append(response['response']['outputSpeech']['text'])

    assert len(RESULTS) >= 3,\
        "should ahve run three times"

    assert RESULTS[0] != RESULTS[1] or RESULTS[1] != RESULTS[2],\
        "should have a random spoken sequence"
