#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

import pytest

import test.requests as requests
from test.conftest import post


resultArr = []


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
    resultArr.append(msg)


def test_get_new_fact_2(client):
    """
    """
    response = post(client, requests.get_new_fact())

    assert response['response']['card'],\
        "should have a card response"

    # add fact to array
    msg = response['response']['outputSpeech']['text']
    resultArr.append(msg)


def test_get_new_fact_3(client):
    """
    """
    response = post(client, requests.get_new_fact())

    # add fact to array
    msg = response['response']['outputSpeech']['text']
    resultArr.append(msg)

    assert len(resultArr) >= 3,\
        "should have run three times"

    assert resultArr[0] != resultArr[1] or resultArr[1] != resultArr[2],\
        "should have a random spoken sequence"
