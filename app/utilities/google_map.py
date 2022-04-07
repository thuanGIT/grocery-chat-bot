import googlemaps as gm
import os
from datetime import datetime
import requests
from app.utilities.logs import Log

# Get the API from Environment Variable
# This API key will be used for all selected API below
__API_KEY = os.getenv("MAP_API_KEY")

# Global object to call GoogleMaps API
gmaps = gm.Client(key=__API_KEY)

Log.d("Google MAP API", "Google MAP API client intialized.")

class GoogleMapDrirection:
    # Log tag
    __TAG = __name__

    def __init__(self):
        self.id = str(datetime.now()).encode("utf-8").hex()
        Log.d(GoogleMapStatic.__TAG, f"GoogleMapDirection instance #{self.id} initalialized.")

    def get_direction_path(self, src, dest, departure_time, mode="driving"):
        """Get the direction from one place to another.

        Args:
            src (str): Source address (Departure Address)
            dest (str): Destination Address
            departure_time (datetime): The time when to depart (default is now)
            mode (str): The transport mode. One of driving”, “walking”, “bicycling” or “transit”

        Returns:
            str: The encoded path to draw on a static map image.
        """
        if departure_time is None:
            departure_time = datetime.now()

        # Call Direction API
        direction_result = gmaps.directions(src, dest, departure_time=departure_time, mode=mode)

        if len(direction_result) < 1:
            Log.e(GoogleMapDrirection.__TAG, "Get direction unsuccessfully.")
            return None
        else:
            Log.i(GoogleMapDrirection.__TAG, "Get direction successfully.")
            return direction_result[0]["overview_polyline"]["points"]

class GoogleMapStatic:
    """A wrapper class for Google Static MAP API to get a static map snapshot.
    """

    # Log TAG
    __TAG = __name__

    def __init__(self):
        self.endpoint = "https://maps.googleapis.com/maps/api/staticmap"
        self.id = str(datetime.now()).encode("utf-8").hex()
        Log.d(GoogleMapStatic.__TAG, f"GoogleMapStatic instance #{self.id} initalialized.")

    def get_map_snapshot(self, lat, lng, zoom=13, size=(300, 300), maptype="roadmap"):
        """Get a snapshot of a map of the current location.

        Args:
            lat (float): Lattitude.
            lng (float): Longtitude
            zoom (int, optional): Zoom level. Defaults to 13.
            size (tuple, optional): Image size. Defaults to (300, 300).
            maptype (str, optional): Map type. Defaults to "roadmap".

        Returns:
            bytes: Image in byte sequence.
        """
        # Constructor params
        params = {
            "center": f"{lat},{lng}",
            "zoom": zoom,
            "size": f"{size[0]}x{size[1]}",
            "format": "jpg",
            "maptype": maptype,
            "markers": f"color:red%7C{lat},{lng}",
            "key": __API_KEY
        }

        # Send the request and get the response body
        response = requests.request(
            method="GET",
            url=self.endpoint,
            params=params
        )

        if response.status_code == 200:
            Log.i(GoogleMapStatic.__TAG, "Get static map successfully.")
            return response.content
        else:
            Log.e(GoogleMapStatic.__TAG, "Get static map failed.")
            return None

    def get_map_path_snapshot(self, origin_lat, origin_lng, path,  size=(512, 512), maptype="roadmap"):
        """Get a snapshot of a map with the specified path

        Args:
            origin_lat (float): The origin's lattitude
            origin_lng (float): The origin's longtitude
            path (str): The overview_polyline returned from Google Direction API
            size (tuple, optional): Image size. Defaults to (512, 512).
            maptype (str, optional): Map type. Defaults to "roadmap".

        Returns:
            bytes: Image in byte sequence.
        """
        params = {
            "size": f"{size[0]}x{size[1]}",
            "format": "jpg",
            "maptype": maptype,
            "visible": f"{origin_lat},{origin_lng}", # Set the origin visible
            "markers": f"color:red|{origin_lat},{origin_lng}", # Mark the destination,
            "path": f"enc:{path}",
            "key": __API_KEY
        }
        response = requests.request(
            method="GET", 
            url=self.endpoint, 
            params=params)

        if response.status_code == 200:
            Log.i(GoogleMapStatic.__TAG, "Get static map with path successfully.")
            return response.content
        else:
            Log.e(GoogleMapStatic.__TAG, "Get static map with path failed.")
            return None


class GoogleMapGeoCoding:
    """A wrapper class for google API client library's Geocoding functionality
    """

    # Log tag
    __TAG = __name__

    def __init__(self):
        self.id = str(datetime.now()).encode("utf-8").hex()
        Log.d(GoogleMapGeoCoding.__TAG, f"GoogleMapStatic instance #{self.id} initalialized.")

    def get_geocoding(self, address):
        """Get the coordinates from the given address

        Args:
            address (str): The address of the place.

        Returns:
            dict: The coordinates {'lat': ..., 'lng': ...}
        """
        # Geocoding an address
        geo_result = gmaps.geocode(address)

        if geo_result:
            Log.i(GoogleMapGeoCoding.__TAG, "GeoCode address sucessfully.")
            return geo_result[0]['geometry']['location']
        else:
            Log.e(GoogleMapGeoCoding.__TAG, "GeoCode address failed.")
            return None
        
    def get_reverse_geocoding(self, lat, lng):
        """Get the address from a coordinate (lattitude, longtitude)

        Args:
            lat (float): Lattitude
            lng (float): Longtitude

        Returns:
            str: The address corresponding to the coordinates
        """
        # Reverse Geocoding a coordinate
        rev_geo_result = gmaps.reverse_geocode((lat, lng))

        if rev_geo_result:
            Log.i(GoogleMapGeoCoding.__TAG, "Revese GeoCode address sucessfully.")
            return rev_geo_result[0]['formatted_address']
        else:
            Log.e(GoogleMapGeoCoding.__TAG, "Revese GeoCode address failed.")
            return None