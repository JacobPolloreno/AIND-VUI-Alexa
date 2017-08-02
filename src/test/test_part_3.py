#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

import json
import re
import test.requests as requests
from test.conftest import post
from test.utils import _read_facts


messages = _read_facts()
fact_msgs = {k: v for k, v in messages.items() if 'get_fact_message'}
facts = {k: v for k, v in messages.items() if 'facts_en_' in k}

resultArr = []


def test_conversational_ele_GetNewFactIntent_1(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    resultArr.append(response['response']['outputSpeech']['text'])

    assert response['response']['reprompt'],\
        "should have reprompt"


def test_conversational_GetNewFactIntent_2(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    resultArr.append(response['response']['outputSpeech']['text'])

    assert response['response']['shouldEndSession'] is not None,\
        "should not end the alexa session"
    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"


def test_conversational_GetNewFactIntent_3(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    resultArr.append(response['response']['outputSpeech']['text'])

    assert response['response']['shouldEndSession'] is not None,\
        "should not end the alexa session"
    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"

    assert len(fact_msgs) >= 5,\
        "should include at least 5 different phrase options"

    assert 

def test_conversational_GetNewFactIntent_valid_year(client):
    facts_str = ' '.join([v for k, v in facts.items()])
    years = re.findall('\d{4}', facts_str)

    if len(years) > 0:
        # Grab invalid year(9999) event
        event = json.load(requests.get_new_year_fact())
        # Modify the year value in the json dict
        event['request']['intent']['slots']['FACT_YEAR']['value'] = years[0]

        response = post(client, json.dumps(event))
    else:
        response = post(client, requests.get_new_year_fact())

    assert response['response']['reprompt'],\
        "should have a reprompt available"

    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"


def test_conversational_GetNewFactIntent_non_matching(client):
    response = post(client, requests.get_new_year_fact())

    assert response['response']['reprompt'],\
        "should have a reprompt available"

    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"
