# Feedback Handler

This documentation will provide an overview of handlers for store and product feedbacks. Currently, no interaction with database is implemented but will be in the future version.

For more information on system architecture, database and APIs, check out [app/README.md](../README.md) and [app/utilities](../utilities/README.md).

## Directory structure

Here's the directory structure of the store_product package.

```bash
.
|- feedback.py      # Feedback handler
|- README.md           
```

## FeedbackHandler

This handler is also a subclass of `BaseHandler`. It checks the sentiment score and return the approriate comments. Currently, only a single message is retuned. In feature version, we hope to return multiple messages for better user experience.

The following table showing the currently supported sentiment cases.

Topics           | Current status
---------------- | --------------  
Positive         | :white_check_mark:
Negative         | :white_check_mark:
Neutral          |

This `handle` method will return a single `str` as the response.

### Usage

To know, which parameters are checked by this handler, please visit the [DialogFlow Console](https://dialogflow.cloud.google.com/#/agent/grocery-chat-bot-v1/intents).

```python
from app.others.feedback import FeedbackHandler

# Prepare arguments (get from Webhook Request json)
kwargs = {
    "intent": str(query_result["intent"]["displayName"]),
    "sentiment": query_result["sentimentAnalysisResult"]
    "params": query_result["parameters"]
}

feedback_handler = FeedbackHandler(session_id=session_id)

# Single str as response
response = feedback_handler.handle(**kwargs)
```

## License

The source files are under MIT license. Please refer to the [LICENSE file](../../LICENSE) for more details.
