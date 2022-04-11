import os
from app.others.feedback_handler import FeedbackHandler
from flask import abort
from app.store_product.product_info import ProductInfoHandler
from app.store_product.store_info import StoreInfoHandler
from app.error import DialogFlowException
from app.utilities.logs import Log


# Define the project id
PROJECT_ID = os.getenv("PROJECT_ID")
class Agent:
    """The main agent to run handler pipeline for generating a response
    """
    # Log TAG
    __TAG = __name__

    def __init__(self, session_id, language_code="en-US"):
        # Custom session id for continuation of conversation
        self.session_id = session_id

        # Handlers
        self.handler_map = {
            "store": StoreInfoHandler(session_id=session_id),
            "product": ProductInfoHandler(session_id=session_id),
            "feedback": FeedbackHandler(session_id=session_id)
        }

    def process(self, query_result):
        """Process the query json.

        Args:
            query_result (dict): The parsed query json.

        Raises:
            DialogFlowException: If unknown intent is found.

        Returns:
            dict: The response in dictionary (called with jsonify in caller)
        """
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
            elif intent_name.startswith("feedback"):
                kwargs["sentiment"] = query_result["sentimentAnalysisResult"]
                json_res["fulfillmentMessages"][0]["text"]["text"].append(self.handler_map["feedback"].handle(**kwargs))
            else: 
                Log.d(Agent.__TAG, "Unknow intent")
                raise DialogFlowException("Unknown intent")
            return json_res
        except Exception as e:
            Log.e(Agent.__TAG, str(e))
            abort(500)