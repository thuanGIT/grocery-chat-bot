# Sample Requests

To help you visualize the Dialogflow API response, we provide a quick way to view the content of the response returned from Dialogflow using `curl` tool.

**Note:** Google service account is required to make requests. Please contact our team if you are a collaborator on this repository.

## Installation & Setup

To run this sample request, you need [Google Cloud SDK CLI](https://cloud.google.com/sdk/docs/install-sdk). Please follow their documentation to have the SDK installed. Once you install the SDK and add it to `PATH`, you should be able to use `gcloud`.

```bash
$ gcloud --version
Google Cloud SDK 380.0.0
bq 2.0.74
core 2022.04.01
gsutil 5.8
```

Now, you need set up environment variables. Here we assume you have the project directory at `$HOME/grocery_chat_bot` and save the service key under `env` directory.

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS="$HOME/grocery-chat-bot/env/dialogflow_key.json"
$ export PROJECT_ID="grocery-chat-bot-v1"
$ export SESSION_ID="123456789"
```

Finally, you just need to edit the provided `request.json` with the nested `text` field with the message to process. The file will look somewhat like this.

```bash
{
  "query_input": {
      "text": {
          "text": "Hi",
          "language_code": "en-US"
      }
  }
}
```

## Usage

```bash
# Change working dir to project_root/example
$ cd grocery_chat_bot/example

# Make a request to the Dialogflow API
$ curl -X POST \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
-d @request.json \
"https://dialogflow.googleapis.com/v2/projects/$PROJECT_ID/agent/sessions/$SESSION_ID:detectIntent"
```

## Output

Below is the output returned from the above request. We hope this will aid in avoiding None type access due to unknow fields.

```bash
{
  "responseId": "13f08532-5ba3-42b2-9d11-034bf8953a0e-7b9a0dae",
  "queryResult": {
    "queryText": "Hi",
    "action": "input.welcome",
    "parameters": {},
    "allRequiredParamsPresent": true,
    "fulfillmentText": "Good day! What can I do for you today?",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Good day! What can I do for you today?"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/grocery-chat-bot-v1/agent/intents/7bde2875-7592-4058-943e-6f2b8db30ce9",
      "displayName": "Default Welcome Intent"
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en"
  }
}
```

## References

- [Usage Guide](https://cloud.google.com/dialogflow/es/docs/quick/api#detect-intent-text-drest)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)

## License

The source files are under MIT license. Please refer to the [LICENSE file](../../LICENSE) for more details.
