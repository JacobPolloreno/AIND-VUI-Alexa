#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
My History Skill
"""

import logging
import random
import os
import yaml

from flask import Blueprint, Flask, render_template
from flask_ask import Ask, statement, question

alexa = Blueprint('alexa', __name__)
ask = Ask(route='/')

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates.yaml')


# TODO (Part 2) add an intent for specifying a fact by year named 'GetNewYearFactIntent'
# TODO (Part 2) provide a function for the new intent named 'GetYearFact'
#     that emits a randomized fact that includes the year requested by the user
#     - if such a fact is not available, tell the user this and provide an alternative fact.
# TODO (Part 3) Keep the session open by providing the fact with 'question'
# instead of 'statement'. Be sure to include a card (e.g 'simple_card') with response.
#     - make sure the user knows that they need to respond
#     - provide a reprompt that lets the user know how they can respond
# TODO (Part 3) Provide a randomized response for the GET_FACT_MESSAGE
#     - add new messages to the templates.yaml file beggining with
#     'get_facts_message_'
#     - randomize this starting portion of the response for conversational
#     variety(already implemented for you, see get_fact() line 49)


@ask.launch
def start():
    return get_fact()


@ask.intent("GetNewFactIntent")
def get_new_fact():
    return get_fact()


@ask.intent("GetFact")
def get_fact():
    with open(TEMPLATES_PATH) as f:
        templates = f.read()

    templates = yaml.load(templates).keys()

    # Select Fact
    factArr = [fact for fact in templates if 'facts_en' in
               fact]
    randomFact = render_template(random.choice(factArr))

    # Select Fact Message (TODO Part 3: Add more)
    factMsgs = [msg for msg in templates if 'get_fact_message' in msg]
    randomMsg = render_template(random.choice(factMsgs))

    # Create speech output
    speechOutput = randomMsg + ' : ' + randomFact

    card_title = render_template('skill_name')
    return statement(speechOutput).simple_card(title=card_title,
                                               content=randomFact)


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
