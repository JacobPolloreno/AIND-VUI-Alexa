#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
My History Facts
"""

import logging
import yaml
import random
import os

from flask import Blueprint, Flask, render_template
from flask_ask import Ask, statement, question, session

alexa = Blueprint('alexa', __name__)
ask = Ask(route='/')

templates_path = os.path.join(os.path.dirname(__file__), 'templates.yaml')

"""
    TODO (Part 2) add messages needed for the additional intent
    TODO (Part 3) add reprompt messages as needed
"""


@ask.launch
def start():
    return get_fact()


@ask.intent("GetNewFactIntent")
def get_new_fact():
    return get_fact()


@ask.intent("GetFact")
def get_fact():
    with open(templates_path) as f:
        templates = f.read()

    templates = yaml.load(templates).keys()
    factArr = [fact for fact in templates if 'facts_en' in
               fact]
    randomFact = render_template(random.choice(factArr))

    # Create speech output
    speechOutput = render_template('get_fact_message') + ':' + randomFact

    card_title = render_template('skill_name')
    return statement(speechOutput).simple_card(title=card_title,
                                               content=randomFact)


"""
    TODO (Part 2) add an intent for specifying a fact by year named 'GetNewYearFactIntent'
    TODO (Part 2) provide a function for the new intent named 'GetYearFact'
        that emits a randomized fact that includes the year requested by the user
        - if such a fact is not available, tell the user this and provide an alternative fact.
    TODO (Part 3) Keep the session open by providing the fact with :askWithCard instead of :tellWithCard
        - make sure the user knows that they need to respond
        - provide a reprompt that lets the user know how they can respond
    TODO (Part 3) Provide a randomized response for the GET_FACT_MESSAGE
        - add message to the array GET_FACT_MSG_EN
        - randomize this starting portion of the response for conversational variety
"""


@ask.intent("AMAZON.HelpIntent")
def help():
    help_text = render_template('help_message')
    return question(help_text).reprompt(help_text)


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement(render_template('stop_message'))


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement(render_template('stop_message'))


@ask.session_ended
def session_ended():
    return "{}", 200


def create_app():
    """
    Initialize a Flask web app instance.

    Other code will use this function as a way to properly construct
    a functional instance of the web app. All environment variable logic is
    handled here and used to wire up the Flask instance.

    :return: new instance of Flask
    """
    app = Flask(__name__)
    app.register_blueprint(alexa)
    ask.init_app(app)

    logger = logging.getLogger("flask_ask")
    logger.setLevel(logging.DEBUG)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
