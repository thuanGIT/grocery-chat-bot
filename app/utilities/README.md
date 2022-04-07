# Utility Modules

This documentation will provide an overview of wrapper modules for APIs, and libraries as utilities for the main and mini conversational agents.

**Note:** APIs keys are required to make requests. Please contact our team if you are a collaborator on this repository.

## Directory structure

Here's the directory structure of the utilities package.

```bash
.                    # utilities directory
|- languages/        # Directory to keep natural language helper
|--- en.py           # English helper module
|- google_map.py     # Google maps API wrapper module
|- logs.py           # Log wrapper module
|- wolfram_alpha.py  # Wolfram|Alpha API wrapper module
|- README.md           
```

## Google Maps Utility

In some scenarios, a user can query the agent for the locations or directions to the grocery stores. While there are many third-party APIs for these functionalities, our team chose GoogleMaps API for its simplicity and ability for scaling.

Here, we use `google-api-python-client` library to help us sending requests to the API suggested by Google Map [documentation](https://cloud.google.com/apis/docs/client-libraries-explained#google_api_client_libraries).

### GoogleMapStatic

The wrapper class `GoogleMapStatic` provides an easy way to get a map snapshot of any locations. Currently, it supports simple snapshots and snapshots with direction path (depends on [GoogleMapDirection](###GoogleMapDirection)).

#### Usage

```python
from app.utilities.google_map import GoogleMapStatic

gm_static = GoogleMapStatic() # Create a GoogleMapStatic instance

# Call method to get an image of map at the coordinates.
# Note: The result is returned in bytes.
# You can use cv2 or write it to disk for viewing
image_bytes = gm_static.get_map_snapshot(-49.89, -109.25, zoom=13, size=(300, 300), maptype="roadmap")

# Call method to get an image of map at the coordinates with direction 
# specified by an encoded path string (from GoogleMapDirection)
# Note: The result is returned in bytes.
# You can use cv2 or write it to disk for viewing
path = "some_encoded path string"
image_with_path_bytes = gm_static.get_map_path_snapshot(-49.89, -109.25, path,  size=(512, 512), maptype="roadmap")
```

### GoogleMapDirection

The wrapper class `GoogleMapDirection` is a convenience way to connect Google Direction API to find directions from two places. Though there are many information in the response, we only extract the encoded path string for `GoogleMapStatic` to display.

#### Usage

```python
from app.utilities.google_map import GoogleMapDirection

gm_direction = GoogleMapDirection() # Create a GoogleMapDirection instance

# Call the method to the encoded path to draw on a static map image.
path_str = gm_direction.get_direction_path(
    "3333 University Way, Kelowna, BC", 
    "1555 Banks Rd, Kelowna, BC", 
    mode="driving")

# Then get a map snapshot with path, for example.
```

### GoogleMapGeocoding

The wrapper class `GoogleMapGeoCoding` gives a quick way to convert address name into a coordinates composed of a latitude, and a longitude. This class also supports the reverse operation (i.e. from coordinates to address name).

#### Usage

```python
from app.utilities.google_map import GoogleMapGeoCoding

gm_geo = GoogleMapGeoCoding() # Create a GoogleMapGeoCoding instance

# Call the method for geocoding an address
coordinates = gm_geo.get_geocoding("3333 University Way, Kelowna, BC")
print(f"({coordinates["lat"]}, {coordinates["lng"]})")

# Call the method for reverse geocoding an address
adresss = gm_geo.get_reverse_geocoding(coordinates["lat"], coordinates["lng"])
print(f"Address: {address}")
```

## Nutrition Utility

To get information on a food product, we use the **Wolfram|Alpha Short Answers API**, which returns an image with all nutritional facts. This will help us reduce the extra data in the database and the hassling to updates.

### Usage

```python
from app.utilities.wolfram_alpha import NutritionQuery

nutrition_q = NutritionQuery.instance() # Get an instance

# Call the method to get the information image in bytes
# Note: You can use cv2 or write to disk to view and process.
image_bytes = nutrition_q.get_nutritional_fact("bananas")
```

## Logs Utility

The module `logs.py` provides a simple wrapper class around the built-in `logging`, following Android API convention. We believe this wrapper will provide a "less-words" and "java-like" way to debug the app.

### Usage

To use this custom log module, the caller calls static methods define in class `Log`. Each one is used in a matching built-case. See [documentation](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) for case explanation.

```python
from app.utilities.logs import Log

# Define a tag for log message
# This will make it easier to search
TAG = __name__

Log.d(TAG, "My message") # Logging verbose (debug case)
Log.i(TAG, "My message") # Logging info case
Log.e(TAG, "My message") # Logging error case
Log.w(TAG, "My message") # Logging warning case
Log.c(TAG, "My message") # Logging critical case
```

## Natural Language Utility

The languages provide support for common operations on natural language (i.e. word forms, grammars). Currently, we are only supporting **English** and **singular <-> plural** noun operations with the help of `inflect` library.

We hope to work on other languages and functionalities in the future.

### Usage

All available operations are defined as static methods under `{language}Util` class. Currently, only `EnglishUtil` is supported.

```python
from app.utilities.languages.en import EnglishUtil

noun = "bananas"

# Check if a noun is plural
if EnglishUtil.is_plural(noun):
    print("Yes! This noun is plural!")

# Convert to plural
EnglishUtil.to_plurals(noun) # Return "bananas"

# Convert to singular
EnglishUtil.to_singular(noun) # Return "banana"
```

## References

- [google-api-python-client 2.43.0](https://pypi.org/project/google-api-python-client/)
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static)
- [Google Directions API](https://developers.google.com/maps/documentation/directions?hl=en_US)
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding)
- [Wolfram|Alpha Short Answers API](https://products.wolframalpha.com/short-answers-api/documentation/)
- [Python logging](https://docs.python.org/3/library/logging.html#module-logging)
- [inflect 5.5.2](https://pypi.org/project/inflect/)

## License

The source files are under MIT license. Please refer to the [LICENSE file](../../LICENSE) for more details.
