from app.agent import Agent
from flask import Flask, jsonify
from datetime import datetime
from app.utilities.logs import Log

# Create a flask app
app = Flask(__name__)
app.config["TAG"] = "Flask App"
app.config["SESSIONS"] = set()
app.config["AGENT"] = Agent()

@app.route("/")
def init_conversation():
  # Create a unique identifier
  session_id = str(datetime.now()).encode("utf-8").hex()
  app.config["SESSIONS"].add(session_id)

  # Logging
  Log.d(app.config["TAG"], f"Conversation id#{session_id} is initialized")

  return jsonify({"session_id": session_id, "status":"OK"})

@app.route("/<session_id>")
def receive_message(session_id):
  # TODO: Get the agent to process message
  ...
