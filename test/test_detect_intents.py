import pytest
from app.agent import Agent
from app.utilities.logs import Log

# Define a sample request data
sample_req = {
  "responseId": "23ed0a46-be5a-4c51-af76-60d875b46cae-7b9a0dae",
  "queryResult": {
    "queryText": "price of banana",
    "parameters": {
      "product": "banana"
    },
    "allRequiredParamsPresent": True,
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/grocery-chat-bot-v1/agent/sessions/0cbc1ecd-bf23-bcf8-a1f4-68e1f5effe19/contexts/__system_counters__",
        "parameters": {
          "no-input": 0,
          "no-match": 0,
          "product": "banana",
          "product.original": "banana"
        }
      }
    ],
    "intent": {
      "name": "projects/grocery-chat-bot-v1/agent/intents/fce457d3-3975-481e-84e6-f253b4d88021",
      "displayName": "product.price"
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en"
  },
  "originalDetectIntentRequest": {
    "source": "DIALOGFLOW_CONSOLE",
    "payload": {}
  },
  "session": "projects/grocery-chat-bot-v1/agent/sessions/0cbc1ecd-bf23-bcf8-a1f4-68e1f5effe19"
}

@pytest.mark.intent_detection
class TestIntentRouting:
    def clean_up():
        Log.d(__name__, "Clean up agent")

    @pytest.fixture
    def agent(self):
        return Agent(session_id="123456789", clean_up=self.clean_up)

    
