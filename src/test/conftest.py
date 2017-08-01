#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tests against My History Skill webapp logic
"""

import json
import os

from index import create_app
# from test.fixtures import *
from pytest import fixture
# from unittest.mock import patch

if 'FLASK_SECRET_KEY' not in os.environ:
    os.environ.setdefault('FLASK_SECRET_KEY', 'asdf')

app = create_app()
app.config['ASK_VERIFY_REQUESTS'] = False
app.config['TESTING'] = True


@fixture(scope='module', name='client')
def setup_client():
    """
    Configure our test fixture. Your test functions have a client
    parameter to allow using pytest fixture.

    :return: Flask test client
    """
    return app.test_client()


def post(flask_client, request):
    """
    Helper function for sending the recorded JSON to our Flask app.

    :param flask_client: Flask test client
    :param request: file descriptor to JSON input

    :return: Python object deserialized from resulting JSON response
    """
    response = flask_client.post('/', data=request)

    # should not have errored
    assert response.status_code == 200
    return json.loads(response.data.decode('utf-8'))
