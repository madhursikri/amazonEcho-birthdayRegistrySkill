Event Regsitry Skill for Amazon Echo
 
# Add an event to the database
1. Save {PersonName} {EventType} as {EventDate}
2. Save {PersonName} {EventType} on {EventDate}
3. Add {PersonName} {EventType} as {EventDate}
4. Add {PersonName} {EventType} on {EventDate}
5. Enter {PersonName} {EventType} as {EventDate}
6. Enter {PersonName} {EventType} on {EventDate}
  
Currently only the following EventType's are supported:

1. birthday
2. anniversary

  
# Retrieve events fom the database
Currently the following methods are supported to retrieve the events from the registry

## Retrieve events by person name and event type. Say any of the following to the amazon echo

1. When is {PersonName} {EventType}

## Retrieve events by event date and event type. Say any of the following to the amazon echo

1. Who all are celebrating their {EventType} {EventDate}
2. Who all have {EventType} {EventDate}

## Retrieve events by event date. Say any of the following to the amazon echo
   
1. what are all the events for {EventDate}
2. what are the events for {EventDate}

Note: You can either give a specific date or say "this week", "next week" etc. 
  
# Alexa Intent Schema
```
{
  "intents": [
    {
      "intent": "Save",
      "slots": [
        {
          "name": "PersonName",
          "type": "AMAZON.US_FIRST_NAME"
        },        
        {
          "name": "EventType",
          "type": "LIST_OF_EVENTS"
        },        
        {
          "name": "EventDate",
          "type": "AMAZON.DATE"
        }
      ]
    },
    {
      "intent": "RetrieveByNameAndType",
      "slots": [
        {
          "name": "PersonName",
          "type": "AMAZON.US_FIRST_NAME"
        }, 
        {
          "name": "EventType",
          "type": "LIST_OF_EVENTS"          
        }
      ]
    },
    {
      "intent": "RetrieveByDateAndType",
      "slots": [
        {
          "name": "EventDate",
          "type": "AMAZON.DATE"
        },
        {
          "name": "EventType",
          "type": "LIST_OF_EVENTS"          
        }        
      ]
    },   
    {
      "intent": "RetrieveByDate",
      "slots": [
        {
          "name": "EventDate",
          "type": "AMAZON.DATE"
        }       
      ]
    }, 
    {
      "intent": "AMAZON.RepeatIntent"
    },
    {
      "intent": "AMAZON.HelpIntent"
    },
    {
      "intent": "AMAZON.StopIntent"
    },
    {
      "intent": "AMAZON.CancelIntent"
    }
  ]
}
```

# Alexa sample utterences
1. Save save {PersonName} {EventType} as {EventDate}
2. Save save {PersonName} {EventType} on {EventDate}
3. Save add {PersonName} {EventType} as {EventDate}
4. Save add {PersonName} {EventType} on {EventDate}
5. Save enter {PersonName} {EventType} as {EventDate}
6. Save enter {PersonName} {EventType} on {EventDate}
7. RetrieveByNameAndType when is {PersonName} {EventType}
8. RetrieveByDateAndType who all are celebrating their {EventType} {EventDate}
9. RetrieveByDateAndType who all have {EventType} {EventDate}
10. RetrieveByDate what are all the events for {EventDate}
11. RetrieveByDate what are the events for {EventDate}


# Alexa custom slot types
1. birthday
2. anniversary
   
