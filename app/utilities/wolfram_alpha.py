from app.utilities.logs import Log
import requests
import os

class NutritionQuery:
    """A wrapper class for Wolfram Summary API for product nutritional facts.
    """
    # Singleton instance
    __instance = None

    # Endpoint
    __endpoint = "https://api.wolframalpha.com/v1/simple"

    # TAG
    TAG = __name__

    # Constructor
    def __init__(self):
        self.WOLFRAM_API_KEY = os.getenv("WOLFRAM_API_KEY")

    # Get the API key
    def instance():
        """Get an instance of NutritionQuery

        Returns:
            NutritionQuery: an instance of NutritionQuery
        """
        if NutritionQuery.__instance:
            return NutritionQuery.__instance
        else:
            NutritionQuery.__instance = NutritionQuery()
            return NutritionQuery.__instance


    def get_nutritional_fact(self, product):
        """Return an image of nutritional facts

        Args:
            product (str): The product name (must be supported in database)

        Returns:
            bytes: The byte sequence representing an image.
        """
        # Construct parameter
        params = {
            "appid": self.WOLFRAM_API_KEY,
            "i": product
        }

        # Start making request to the endpoint
        response = requests.request(
            method="GET",
            url=NutritionQuery.__endpoint,
            params=params
        )

        success = response.status_code == 200
        # Logging
        Log.i(NutritionQuery.TAG, "Summary is successful" if success  else response.content.decode(response.encoding))
        return response.content if success else None