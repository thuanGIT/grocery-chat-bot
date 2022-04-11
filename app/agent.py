import os
from flask import abort
from app.store_product.product_info import ProductInfoHandler
from app.store_product.store_info import StoreInfoHandler
from app.error import DialogFlowException
from app.utilities.logs import Log


# Define the project id
PROJECT_ID = os.getenv("PROJECT_ID")
class Agent:
    """The main agent to facilitate the conversation with customers. Its backend is set up
    with mini-agents and Diagflow API.
    
    Attributes:
        session_id: Unique session id for each conversation
        session_client: session client object for dialogflow
        language_code: language code for dialogflow, default to en-US
        session: session path for dialogflow
        intents: dictionary of current intents the bot handles
        tolerant_count: Counts of undetected intents
    """
    # Log TAG
    __TAG = __name__

    def __init__(self, session_id, language_code="en-US"):
        # Custom session id for continuation of conversation
        self.session_id = session_id

        # Handlers
        self.handler_map = {
            "store": StoreInfoHandler(session_id=session_id),
            "product": ProductInfoHandler(session_id=session_id)
        }

    def process(self, query_result):
        try:
            # Get the intent's display name
            intent_name = str(query_result["intent"]["displayName"])

            # Prepare the json response
            json_res = {
                "fulfillmentMessages": [
                {
                    "text": {
                        "text": []
                    }
                }
                ]
            }

            # Mini-agent to handle business logics
            # If conversation is starting | ending | inable to understand
            kwargs = {
                "intent": intent_name,
                "params": query_result["parameters"]
            }
            if intent_name.startswith("default"): 
                json_res["fulfillmentMessages"][0]["text"]["text"].append(query_result.fulfillment_messages[0].text.text)
            elif intent_name.startswith("store"):
                # Set up configurations
                json_res["fulfillmentMessages"][0]["text"]["text"].append(self.handler_map["store"].handle(**kwargs))
            elif intent_name.startswith("product"):
                json_res["fulfillmentMessages"][0]["text"]["text"].append(self.handler_map["product"].handle(**kwargs))
            else: 
                Log.d(Agent.__TAG, "Unknow intent")
                raise DialogFlowException("Unknown intent")
            return json_res
        except Exception as e:
            Log.e(Agent.__TAG, str(e))
            abort(500)