from flask import Blueprint, request, jsonify, render_template
from app.extensions import mongo
import datetime

webhook = Blueprint('Webhook', __name__)

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json

    if data:
        event_type = request.headers.get('X-GitHub-Event')
        event = {
            "event_type": event_type,
            "event_data": data,
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
        }
        mongo.db.events.insert_one(event)
        return jsonify({"message": "Event received"}), 200

    return jsonify({"message": "No data received"}), 400

@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)
    response = []
    for event in events:
        author = event["event_data"]["sender"]["login"]
        timestamp = event["timestamp"]
        action = event["event_type"]
        if action == "push":
            branch = event["event_data"]["ref"].split("/")[-1]
            action = "pushed to"
        elif action == "pull_request":
            branch = event["event_data"]["pull_request"]["base"]["ref"]
            action = "submitted a pull request from"
        elif action == "merge":
            branch = event["event_data"]["pull_request"]["base"]["ref"]
            action = "merged branch"
        response.append({"author": author, "action": action, "branch": branch, "timestamp": timestamp})
    return jsonify(response)

@webhook.route('/', methods=["GET"])
def index():
    return render_template('index.html')
