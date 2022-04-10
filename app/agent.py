import sys
import os
from google.cloud import dialogflow
from flask import abort
from app.store_product.product_info import ProductInfoHandler
from app.store_product.store_info import StoreInfoHandler
from app.concerns.other_concern import OtherConcernsHandler
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

        # Only one session client for one customer
        self.session_client = dialogflow.SessionsClient()

        # Get the qualified session string (id)
        self.session = self.session_client.session_path(PROJECT_ID, self.session_id)

        # Configurations
        self.language_code = language_code

        # Handlers
        self.handler_map = {
            "store": StoreInfoHandler(),
            "product": ProductInfoHandler()
        }

    def process(self, message):
        """Process the user message and return the response message.

        Args:
            message (str): The user message

        Raises:
            HttpException: An error occurs during processing (aborting with code 500)

        Returns:
            dict: The json to return to client
        """
        try:
            # Call DiagFlow API
            query_result = self.detect_message_intent(message=message)
            Log.i(Agent.__TAG, "Dialogflow API call succeeded!")

            # Get the intent's display name
            intent = str(query_result.intent.display_name)

            # Prepare the json response
            json_res = {"response_message": ""}

            # Mini-agent to handle business logics
            # If conversation is starting | ending | inable to understand
            kwargs = {
                "intent": intent,
                "params": query_result.parameters
            }
            if intent.startswith("default"): 
                json_res["response_message"] = query_result.fulfillment_messages[0].text.text
            elif intent.startswith("store"):
                # Set up configurations
                json_res["response_message"] = self.handler_map["store"].handle(**kwargs)
            elif intent.startswith("product"):
                json_res["response_message"] = self.handler_map["product"].handle(**kwargs)
            else: 
                Log.d(Agent.__TAG, "Unknow intent")
                raise DialogFlowException("Unknown intent")
            return json_res
        except Exception as e:
            Log.e(Agent.__TAG, "Dialogflow API call failed:", str(e))
            abort(500)
        
    
    def detect_message_intent(self, message):
        """Detect intent with Dialogflow API for the current message.

        Args:
            message (str): The user's message

        Raises:
            DialogFlowException: "Dialogflow API error" if cannot connect to dialogflow

        Returns:
            QueryResult: The query result from Dialogflow API
        """
        try:
            # Process text_input
            text_input = dialogflow.TextInput(text=message, language_code=self.language_code)
            
            # Call Dialogflow API
            query_input = dialogflow.QueryInput(text=text_input)

            response = self.session_client.detect_intent(
                request={"session": self.session, "query_input": query_input}
            )
            return response.query_result
        except Exception:
            raise DialogFlowException("Dialogflow API error")

