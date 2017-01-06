Event Regsitry Skill for Amazon Echo
 
# Add an event to the database
  TODO
  
# Retrieve events fom the database
  TOOD
  
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
Save save {PersonName} {EventType} as {EventDate}
Save save {PersonName} {EventType} on {EventDate}
Save add {PersonName} {EventType} as {EventDate}
Save add {PersonName} {EventType} on {EventDate}
Save enter {PersonName} {EventType} as {EventDate}
Save enter {PersonName} {EventType} on {EventDate}
RetrieveByNameAndType when is {PersonName} {EventType}
RetrieveByDateAndType who all are celebrating their {EventType} {EventDate}
RetrieveByDateAndType who all have {EventType} {EventDate}
RetrieveByDate what are all the events for {EventDate}
RetrieveByDate what are the events for {EventDate}


# Alexa custom slot types
birthday
anniversary
   
