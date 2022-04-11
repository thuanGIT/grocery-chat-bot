from datetime import datetime
from app.base_handler import BaseHandler
from app.error import SQLException
from app.utilities.google_map import GoogleMapDirection, GoogleMapStatic, GoogleMapGeoCoding
from app.utilities.logs import Log

class StoreInfoHandler(BaseHandler):
    """A class used to represent a mini-agent to handle store queries.
    """

    def __init__(self, session_id) -> None:
        super().__init__(session_id=session_id)
        self.source = None

    def handle(self, **kwargs):
        # Get the intent name & parameters
        intent_name = str(kwargs["intent"])
        params = kwargs["params"]

        # Get the sub-intent
        sub_intent = intent_name[intent_name.index(".") + 1:]

        if sub_intent.startswith("location"):
            if sub_intent == "location - yes":
                return self.get_direction(source=self.source)
            else:  # Just location
                # Get action
                action = params["store_action_location"]
                if action == "address":
                    return self.get_address()
                else: # Action = directions
                    source_address = params["address"]
                    if len(str(source_address)) > 0:
                        self.source = str(source_address)
                        return "Would you want a direction to the store from here?"
                    else:
                        return "Please tell me your departure location."
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

    def get_direction(self, source):
        """Get the direction to store.

        Args:
            source (str): The source address

        Returns:
            bytes: The image showing the direction.
        """
        gm_direction = GoogleMapDirection() # Create a GoogleMapDirection instance

        # Call the method to the encoded path to draw on a static map image.
        path_str = gm_direction.get_direction_path(
            source, 
            self.get_address(),
            departure_time=datetime.now(),
            mode="driving")

        # Decode source address
        gm_geo = GoogleMapGeoCoding() # Create a GoogleMapGeoCoding instance
        coordinates = gm_geo.get_geocoding(source)

        gm_static = GoogleMapStatic() # Create a GoogleMapStatic instance
        return gm_static.get_map_path_snapshot(coordinates["lat"], coordinates["lng"], path_str, size=(512, 512), maptype="roadmap")
        
        
