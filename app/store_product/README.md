# Product & Store Handlers

This documentation will provide an overview of handlers for store and product queries.
Handlers are backed by the store database (PostgreSQL) and third-party APIs. All handlers are subclasses of `BaseHandler`.

For more information on system architecture, database and APIs, check out [app/README.md](../README.md) and [app/utilities](../utilities/README.md).

## Directory structure

Here's the directory structure of the store_product package.

```bash
.
|- product_info.py      # Product handler
|- store_info.py        # Store handler
|- README.md           
```

## StoreInfoHandler

This handler queries the database mostly on the `Store` table for store information. It also uses GoogleMaps API to get store location and directions on a static image.

The following table showing the currently supported topics.

Topics          | Current status
----------------| --------------  
Address         | :white_check_mark:
Direction       | :white_check_mark:
Opening Hours   | :white_check_mark:
Contact         | :white_check_mark:
Price Range     |
Reviews         |

This `handle` method will return `str|bytes` depending on whether it is returning a text or an image. The processing of putting the image in response json is done by main agent.

### Usage

To know, which parameters are checked by this handler, please visit the [DialogFlow Console](https://dialogflow.cloud.google.com/#/agent/grocery-chat-bot-v1/intents).

```python
from app.store_product.store_info import StoreInfoHandler

# Prepare arguments (get from Webhook Request json)
kwargs = {
    "intent": str(query_result["intent"]["displayName"]),
    "params": query_result["parameters"]
}

store_handler = StoreInfoHandler(session_id=session_id)

# Could be str for text or bytes for image
response = store_handler.handle(**kwargs)
```

## ProductInfoHandler

This handler queries the database mostly on the `Product` table for product information. It also uses Wolfram|Alpha Short Answers API to get a product nutritional facts.

The following table showing the currently supported topics.

Topics          | Current status
----------------| --------------  
Price           | :white_check_mark:
Price In Bulks  |
Nutrition       | :white_check_mark:
Stock (boolean) | :white_check_mark:
Exchange/Refund | :white_check_mark:
Reviews         |

This `handle` method will return `str|bytes` depending on whether it is returning a text or an image. The processing of putting the image in response json is done by main agent.

### Usage

To know, which parameters are checked by this handler, please visit the [DialogFlow Console](https://dialogflow.cloud.google.com/#/agent/grocery-chat-bot-v1/intents).

```python
from app.store_product.product_info import ProductInfoHandler

# Prepare arguments (get from Webhook Request json)
kwargs = {
    "intent": str(query_result["intent"]["displayName"]),
    "params": query_result["parameters"]
}

store_handler = ProductInfoHandler(session_id=session_id)

# Could be str for text or bytes for image
response = store_handler.handle(**kwargs)
```

## License

The source files are under MIT license. Please refer to the [LICENSE file](../../LICENSE) for more details.
