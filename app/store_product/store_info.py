from pytest import param
from app.base_handler import BaseHandler
from app.error import SQLException

class StoreInfoHandler(BaseHandler):
    """A class used to represent a mini-agent to handle store queries.
    """

    def __init__(self) -> None:
        super().__init__()

    def handle(self, **kwargs):
        # Get the intent name & parameters
        intent_name = str(kwargs["intent"])
        params = kwargs["params"]

        # Get the sub-intent
        sub_intent = intent_name[intent_name.index(".") + 1:]

        if sub_intent == "location":
            # Get action
            action = params["store_action_location"]
            if action == "address":
                return self.get_address()
            else: ... # TODO: Add handler for direcion
        elif sub_intent == "open_hours":
            # Get hours
            hours = self.get_hours().split("-")
            # Get action
            action = params["store_action_open_hours"]
            return hours[0].strip() if action == "open" else hours[1].strip()
        elif sub_intent == "contact":
            # Get action
            action = params["store_action_contact"]
            if action == "website":
                return self.get_website()    
            elif action == "phone":
                return self.get_phone()
            else: 
                raise SQLException("No action found!")
        else:
            raise SQLException("Not sub-intent found!")


    def get_address(self) -> str:
        """Get store location (only 1 store).

        Returns:
            str: The address of the store.
        """
        results = self.db.execute("SELECT Address FROM Store;")
        return list(results)[0][0]

    def get_hours(self) -> str:
        """Get store working hours (only 1 store)

        Returns:
            str: Open-close hours
        """
        results = self.db.execute("SELECT OpeningHours FROM Store;")
        return list(results)[0][0]

    def get_website(self):
        """Get the store website.

        Returns:
            str: The store website
        """
        results = self.db.execute("SELECT Website FROM Store;")
        return list(results)[0][0]

    def get_phone(self):
        """Get the store phone number.

        Returns:
            str: The store phone number.
        """
        results = self.db.execute("SELECT PhoneNumber FROM Store;")
        return list(results)[0][0]