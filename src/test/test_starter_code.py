#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""
import test.requests as requests
from test.conftest import post

import pytest

RESULTS = []


def test_cancel(client):
    """
    User should be able to cancel the interactions according to Amazon

    :param client
    """
    response = post(client, requests.cancel())

    assert response['response']['shouldEndSession'],\
        "should end the alexa session"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    with pytest.raises(KeyError, message="should have no reprompt"):
        response['response']['reprompt']


def test_stop(client):
    """
    User should be able to stop the interactions according to Amazon

    :param client
    """
    response = post(client, requests.stop())

    assert response['response']['shouldEndSession'],\
        "should end the alexa session"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    with pytest.raises(KeyError, message="should have no reprompt"):
        response['response']['reprompt']


def test_help(client):
    """
    User should be able to ask for help and also be reprompted

    :param client
    """
    response = post(client, requests.help())

    assert response['response'],\
        "should have a speechlet response"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    assert response['response']['reprompt'],\
        "should have a reprompt available"

    assert response['response']['shouldEndSession'] is not None,\
        "should not end the alexa session"
    assert not response['response']['shouldEndSession'],\
        "should not end the alexa session"


def test_get_new_fact_1(client):
    """
    """
    response = post(client, requests.get_new_fact())

    assert response['response'],\
        "should have a speechlet response"

    assert response['response']['outputSpeech'],\
        "should have a spoken response"

    # add fact to array
    msg = response['response']['outputSpeech']['text']
    RESULTS.append(msg)


def test_get_new_fact_2(client):
    """
    """
    response = post(client, requests.get_new_fact())

    assert response['response']['card'],\
        "should have a card response"

    # add fact to array
    msg = response['response']['outputSpeech']['text']
    RESULTS.append(msg)


def test_get_new_fact_3(client):
    """
    """
    response = post(client, requests.get_new_fact())

    # add fact to array
    msg = response['response']['outputSpeech']['text']
    RESULTS.append(msg)

    assert len(RESULTS) >= 3,\
        "should have run three times"

    assert RESULTS[0] != RESULTS[1] or RESULTS[1] != RESULTS[2],\
        "should have a random spoken sequence"
