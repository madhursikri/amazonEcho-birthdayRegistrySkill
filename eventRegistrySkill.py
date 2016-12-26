import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    print("intent_request_json: " + json.dumps(intent_request, indent=4, sort_keys=True))

    intent_name = intent_request['intent']['name']
    print("intent name was: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "Save":
        return SaveEventHandler.save_event(intent_request)
    else:
        raise ValueError("Invalid intent")

class SaveEventHandler:

    @staticmethod
    def save_event(intent_request):
        """ Sets the phrase in dynamo DB and prepares the speech to reply to the user."""

        card_title = intent_request['intent']['name']

        person_name = intent_request['intent']['slots']['PersonName']['value']
        event_type = intent_request['intent']['slots']['EventType']['value']
        event_date = intent_request['intent']['slots']['EventDate']['value']

        # persist in database
        #{
        #    "person_name" : "person_name",
        #    "event_type" : "event_type",
        #    "event_date" : "event_date",
        #    "created_date": "today's date/time"
        #}
        jsonData = '{"person_name": person_name, "event_type": event_type, "event_date":event_date, "created_date": dateTime.now()}'
        print("json to add to db:" + jsonData)
        print("Putting data in dynamodb. Saving " + event_type + " for " + person_name + " as " + event_date)

        SaveEventHandler.save_in_db(person_name, event_date, jsonData )
        reprompt_text = ""

        speech_output = "Saved " + event_type + " for " + person_name + " as " + event_date
        return build_response({}, build_speechlet_response(title=card_title,
                                                           output=speech_output,
                                                           reprompt_text=reprompt_text,
                                                           should_end_session=True))

    @staticmethod
    def save_in_db(person_name, event_date, payload):

        # get connection to dynamo
        dynamo = boto3.resource('dynamodb')

        # get table
        table = dynamo.Table('EventRegistry')

        table.put_item(Item={
            'person_name': person_name,
            'event_date': event_date,
            'event_details': {
                payload
            }
        })

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the event registry. " \
                    "To save an event, for example a birthday, please say 'Save John's birthday as Jan 1 1984'"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Totally didn't understand that."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
