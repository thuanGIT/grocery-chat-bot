from flask import Flask, jsonify, abort, request, send_file
from app.agent import Agent
from app.utilities.logs import Log
import base64
import os

# Get authentications from env variables
AUTH_USER = os.getenv("AUTH_USER")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

# Create a flask app
app = Flask(__name__)
app.config["TAG"] = "Flask App"
app.config["AGENTS"] = dict()
app.config["AUTH"] = f"{AUTH_USER}:{AUTH_PASSWORD}"

@app.route("/", methods=["POST"])
def webhook():
  # Get authentication values
  auth = base64.b64decode(request.headers.get("Authorization").split(" ")[1])
  # Check auth
  if auth.decode("utf-8") == app.config["AUTH"]:
    # Get the sessions
    session_id = str(request.json["session"]).split("/")[-1]
    # Get the agent
    agent = app.config["AGENTS"].setdefault(session_id, Agent(session_id=session_id))
    # Process the request json and return the response
    return agent.process(request.json["queryResult"])
  else:
    abort(400)
  
@app.route("/image/<session_id>", methods=["GET"])
def get_image(session_id):
  Log.d(app.config["TAG"], "Getting images")
  path = f"/tmp/image_{session_id}.png"
  return send_file(path)

@app.errorhandler(500)
def handle_server_error(e):
  Log.e(app.config["TAG"], str(e))
  return {}, 500

@app.errorhandler(400)
def handle_client_error(e):
  Log.e(app.config["TAG"], str(e))
  return jsonify({"error": "Bad Request!"}), 400