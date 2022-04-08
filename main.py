from http.client import HTTPException
from app.agent import Agent
from flask import Flask, jsonify, abort
from datetime import datetime
from app.utilities.logs import Log

# Create a flask app
app = Flask(__name__)
app.config["TAG"] = "Flask App"
app.config["AGENTS"] = dict()

@app.route("/")
def init_conversation():
  # Create a unique identifier
  session_id = str(datetime.now()).encode("utf-8").hex()
  app.config["AGENTS"][session_id] = Agent(session_id=session_id)

  # Logging
  Log.d(app.config["TAG"], f"Conversation id#{session_id} is initialized")

  return jsonify({
    "session_id": session_id,
    "welcome_message": "Hello, welcome to the official chatbot of The Store. How can I help you today?"
    })

@app.route("/<session_id>")
def receive_message(session_id):
  try:
    # Get the agent
    agent = app.config["AGENTS"][session_id]

    # Logging
    Log.i(app.config["TAG"], "Agent found!")

    # TODO: Get the agent to process message
  except Exception as e:
    if e is HTTPException:
      raise e
    Log.e(app.config["TAG"], str(e))
    abort(400)
    
    
@app.errorhandler(500)
def handle_server_error(e):
  return {}, 500

@app.errorhandler(400)
def handle_client_error(e):
  return jsonify({"error": "Bad Request!"}), 400