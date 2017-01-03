import json
import boto3
import uuid
from datetime import datetime, timedelta, date
import calendar
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the requesst is provided in the event parameter.
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
    #print("intent_request_json: " + json.dumps(intent_request, indent=4, sort_keys=True))

    intent_name = intent_request['intent']['name']
    print("intent name was: " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "Save":
        return EventRegistry.save_event(intent_request)
    elif intent_name == "RetrieveByNameAndType":
        return EventRegistry.retrieve_events_by_name_and_type(intent_request)
    elif intent_name == "RetrieveByDateAndType":
        return EventRegistry.retrieve_events_by_date_and_type(intent_request)
    elif intent_name == "RetrieveByDate":
        return EventRegistry.retrieve_events_by_date(intent_request)
    else:
        raise ValueError("Invalid intent")

class EventRegistry:

    @staticmethod
    def save_event(intent_request):
        """ Saves the event in dynamo db and prepares the speech to reply to the user."""

        card_title = intent_request['intent']['name']

        person_name = intent_request['intent']['slots']['PersonName']['value']
        event_type = intent_request['intent']['slots']['EventType']['value']
        event_date = intent_request['intent']['slots']['EventDate']['value'][5:]

        # persist in database
        #{
        #    "uuid" : uuid,
        #    "person_name" : person_name,
        #    "event_type" : event_type,
        #    "event_date" : event_date,
        #    "created_date_time_utc": today's date/time
        #}

        # get connection to dynamo
        dynamo = boto3.resource('dynamodb')

        # get table
        table = dynamo.Table('event_registry')

        table.put_item(Item={
            'uuid': str(uuid.uuid4()),
            'person_name': person_name,
            'event_type': event_type,
            'event_date': event_date,
            'created_date_time_utc': datetime.utcnow().isoformat()
        })

        print("Successfully added data to dynamodb. Saved " + event_type + " for " + person_name + " as " + event_date)

        reprompt_text = ""

        # convert event_date (01-01) to Jan 01
        event_month = event_date[:2]
        event_day = event_date[3:]

        event_date_in_format = calendar.month_name[int(event_month)] + " " + event_day

        speech_output = "Saved " + person_name + " " + event_type + " as " + event_date_in_format + "."
        return build_response({}, build_speechlet_response(title=card_title,
                                                           output=speech_output,
                                                           reprompt_text=reprompt_text,
                                                           should_end_session=True))

    @staticmethod
    def retrieve_events_by_name_and_type(intent_request):

        person_name = intent_request['intent']['slots']['PersonName']['value']
        event_type = intent_request['intent']['slots']['EventType']['value']

        print("Retrieving " + event_type + " for " + person_name)

        # get connection to dynamo
        dynamo = boto3.resource('dynamodb')

        # get table
        table = dynamo.Table('event_registry')

        response = table.scan(
                FilterExpression=Key('person_name').eq(person_name) & Key('event_type').eq(event_type)
        )

        #print(response)
        if len(response['Items']) > 0:
            # convert event_date (01-01) to Jan 01
            event_date = response['Items'][0]['event_date']
            event_month = event_date[:2]
            event_day = event_date[3:]

            event_date_in_format = calendar.month_name[int(event_month)] + " " + event_day

            speech_output = event_type + " for " + person_name + " is on " + event_date_in_format
        else:
            speech_output = event_type + " for " + person_name + " was not found. Please add the event to the registry first."



        return build_response(session_attributes={},
                              speechlet_response=build_speechlet_response("Repeat", speech_output, "", True))

    @staticmethod
    def retrieve_events_by_date_and_type(intent_request):

        event_date = intent_request['intent']['slots']['EventDate']['value'][5:]
        event_type = intent_request['intent']['slots']['EventType']['value']

        print("Retrieving " + event_type + " for " + event_date)

        # get connection to dynamo
        dynamo = boto3.resource('dynamodb')

        # get table
        table = dynamo.Table('event_registry')

        response = table.scan(
                FilterExpression=Key('event_date').eq(event_date) & Key('event_type').eq(event_type)
        )

        #print(response)

        # convert event_date (01-01) to Jan 01
        event_month = event_date[:2]
        event_day = event_date[3:]

        event_date_in_format = calendar.month_name[int(event_month)] + " " + event_day

        if len(response['Items']) > 0:
            speech_output = "The following people have " + event_type + " on " + event_date_in_format + ","

            for i in response['Items']:
                speech_output = speech_output + i['person_name'] + ", "
        else:
            speech_output = "No " + event_type + " falling on " + event_date_in_format + " were found."

        return build_response(session_attributes={},
                              speechlet_response=build_speechlet_response("Repeat", speech_output, "", True))

    @staticmethod
    def retrieve_events_by_date(intent_request):

        event_date = intent_request['intent']['slots']['EventDate']['value']

        print("Retrieving events for " + event_date)

        # get connection to dynamo
        dynamo = boto3.resource('dynamodb')

        # get table
        table = dynamo.Table('event_registry')

        speech_output = ""
        # check if the request is for a week
        if "W" in event_date:
            start_date = tofirstdayinisoweek(int(event_date[:4]), int(event_date[-2:]))
            end_date = start_date + timedelta(days=6)

            #print("start date is" + start_date.strftime('%m-%d'))
            #print("end date is" + end_date.strftime('%m-%d'))

            response = table.scan(
                    FilterExpression=Key('event_date').between(start_date.strftime('%m-%d'), end_date.strftime('%m-%d')))

            start_event_month = start_date.strftime('%m-%d')[:2]
            start_event_day = start_date.strftime('%m-%d')[3:]
            start_event_date_in_format = calendar.month_name[int(start_event_month)] + " " + start_event_day

            end_event_month = end_date.strftime('%m-%d')[:2]
            end_event_day = end_date.strftime('%m-%d')[3:]
            end_event_date_in_format = calendar.month_name[int(end_event_month)] + " " + end_event_day


            speech_output = " Events between " + start_event_date_in_format + " and " + end_event_date_in_format + " are:"

            if len(response['Items']) > 0:
                for i in response['Items']:
                    date_from_db = i['event_date']
                    # convert event_date (01-01) to Jan 01
                    event_month = date_from_db[:2]
                    event_day = date_from_db[3:]

                    event_date_in_format = calendar.month_name[int(event_month)] + " " + event_day
                    speech_output = speech_output + i['event_type'] + " for " + i['person_name']  + " on " + event_date_in_format
            else:
                speech_output = "No events falling between " + start_event_date_in_format + " and " + end_event_date_in_format + " were found."
        else:
            # remove the year before quering the database.
            event_date = event_date[5:]
            response = table.scan(
                    FilterExpression=Key('event_date').eq(event_date)
            )

            # convert event_date (01-01) to Jan 01
            event_month = event_date[5:-3]
            event_day = event_date[8:]

            event_date_in_format = calendar.month_name[int(event_month)] + " " + event_day
            speech_output = "Events for " + event_date_in_format + " are "

            if len(response['Items']) > 0:
                for i in response['Items']:
                    speech_output = speech_output + i['event_type'] + " for " + i['person_name']
            else:
                speech_output = "No events falling on " + event_date_in_format + " were found."

        return build_response(session_attributes={},
                              speechlet_response=build_speechlet_response("Repeat", speech_output, "", True))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the event registry. " \
                    "To add an event, for example a birthday, please say 'Add John birthday as Jan 1 1984'"
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

def tofirstdayinisoweek(year, week):
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret
