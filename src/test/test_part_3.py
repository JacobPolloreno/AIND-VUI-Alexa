#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests Part 3 against My History Skill webapp logic
"""

import json
import pytest
import re
import test.requests as requests
from test.conftest import post
from test.utils import _read_facts, get_num_included_phrases, has_year_intent_schema


MESSAGES = _read_facts()
FACT_MSGS = {k: v for k, v in MESSAGES.items() if 'get_fact_message_' in k}
FACTS = {k: v for k, v in MESSAGES.items() if 'facts_en_' in k}
RESULTS = []

# Instead of getting a NotImplementedError with long debuggin output,
# we can skip some of the test and output a reason to make reading
# the test easier.
SKIP_REASON = """
    Not Implemented Error:
        should include 'GetNewYearFactIntent' in
        IntentSchema.json first then continue testing.
        This test will not be skipped afterwards.
"""


def test_conv_getnewfactintent_1(client):
    """
    User should get a new fact and be reprompted

    :param client
    """
    response = post(client, requests.get_new_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    RESULTS.append(response['response']['outputSpeech']['text'])

    assert response['response']['reprompt'],\
        "should have reprompt"


def test_conv_getnewfactintent_2(client):
    """
    User should get a new fact and Amazon should keep the session open

    :param client
    """
    response = post(client, requests.get_new_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    RESULTS.append(response['response']['outputSpeech']['text'])

    assert response['response']['shouldEndSession'] is not None,\
        "should not end the alexa session"
    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"


def test_conv_getnewfactintent_3(client):
    """
    User should get a new fact, Amazon should keep the session open,
    and should include at least 5 different phrase options to prefix
    the get fact message. Further, the prefix should be randomly
    assigned.

    :param client
    """
    response = post(client, requests.get_new_fact())

    assert response['response']['outputSpeech']['text'],\
        "should have a response"

    RESULTS.append(response['response']['outputSpeech']['text'])

    assert response['response']['shouldEndSession'] is not None,\
        "should not end the alexa session"
    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"

    assert len(FACT_MSGS) >= 5,\
        "should include at least 5 different phrase options"

    assert get_num_included_phrases(RESULTS, FACT_MSGS),\
        "should randomly include segments from the GET_FACT_MESSAGE templates"


@pytest.mark.skipif(not has_year_intent_schema(),
                    reason=SKIP_REASON)
def test_conv_getnewyearfactintent_valid_year(client):
    """
    User should get a new fact based on a valid year, Amazon
    should keep the session open, and should reprompt user.

    :param client
    """

    # Get some valid years
    facts_str = ' '.join([v for k, v in FACTS.items()])
    years = re.findall(r'\d{4}', facts_str)

    if not years:
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


@pytest.mark.skipif(not has_year_intent_schema(),
                    reason=SKIP_REASON)
def test_conv_getnewyearfactintent_non_matching(client):
    """
    User should get a new fact based on a invalid year, Amazon
    should keep the session open, and should reprompt user.

    :param client
    """
    response = post(client, requests.get_new_year_fact())

    assert response['response']['reprompt'],\
        "should have a reprompt available"

    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"
