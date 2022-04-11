import os
from app.others.feedback_handler import FeedbackHandler
from flask import abort, url_for, request
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

            response = None
            if intent_name.startswith("default"):
                sub_intent = intent_name[intent_name.index(".") + 1:]
                if sub_intent == "done":
                    for _, handler in self.handler_map.items():
                        handler.dispose()
                response = query_result["fulfillmentMessages"][0].text.text
            elif intent_name.startswith("store"):
                response = self.handler_map["store"].handle(**kwargs)
            elif intent_name.startswith("product"):
                response = self.handler_map["product"].handle(**kwargs)
            elif intent_name.startswith("feedback"):
                kwargs["sentiment"] = query_result["sentimentAnalysisResult"]
                response = self.handler_map["feedback"].handle(**kwargs)
            else: 
                Log.d(Agent.__TAG, "Unknow intent")
                raise DialogFlowException("Unknown intent")

            # Check type
            if isinstance(response, bytes):
                    self.save_image_tmp(response, self.session_id)
                    path = url_for("get_image", session_id = self.session_id)
                    # Get the base url (replace with https and remove path /)
                    base_url = request.base_url.replace("http", "https")[:-1]
                    full_path = f"{base_url}{path}"
                    Log.d(Agent.__TAG, full_path)
                    json_res["fulfillmentMessages"].append(
                        {
                            "payload": {
                                "richContent": [
                                    [
                                        {
                                            "rawUrl": full_path,
                                            "type": "image",
                                            "accessibilityText": "Directions" if intent_name.startswith("store") else "Nutritions"
                                        }
                                    ]
                                ]
                            }
                        }
                    )
                    # Add a simple message
                    json_res["fulfillmentMessages"][0]["text"]["text"].append("Here you are!")                    
            else:
                json_res["fulfillmentMessages"][0]["text"]["text"].append(response)
            return json_res
        except Exception as e:
            Log.e(Agent.__TAG, str(e))
            abort(500)

    def save_image_tmp(self, image: bytes, id):
        path = f"/tmp/image_{id}.png"
        with open(path, "wb") as f:
            f.write(image)
        return path
    
