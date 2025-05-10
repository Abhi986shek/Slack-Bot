from flask import Flask, request, jsonify
from slack_bolt import App  # Slack Bolt SDK
from slack_bolt.adapter.flask import SlackRequestHandler
import logging


# Configuration
BOT_TOKEN = ""  # Slack Bot Token
SIGNING_SECRET = ""  # Slack Signing Secret


# Logger Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Slack App Initialization
slack_app = App(token=BOT_TOKEN, signing_secret=SIGNING_SECRET)

# Flask app initialization
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)


# Route: Slack Events
@flask_app.route("/slack/events/<event_id>", methods=["POST"])
def slack_events(event_id):
    """
    Handles incoming Slack events via the Events API.
    Supports URL verification and responds to user messages.

    Args:
        event_id (str): Unique identifier for the event path.

    Returns:
        Flask Response: JSON response indicating event handling result.
    """
    data = request.get_json()

    # Handle Slack URL verification challenge
    if "challenge" in data:
        logger.info(f"Received Slack URL verification challenge for event_id: {event_id}")
        return jsonify({"challenge": data["challenge"]})

    # Handle Slack message events
    event = data.get("event", {})
    if event.get("type") == "message" and "subtype" not in event and "client_msg_id" in event:
        user_id = event.get("user")
        channel_id = event.get("channel")
        text = event.get("text")

        logger.info(f"Slack Message Event - ID: {event_id}, User: {user_id}, Channel: {channel_id}, Text: {text}")

        # Respond immediately to Slack
        response = jsonify({"status": "ok"})

        # Echo message back to the channel
        slack_app.client.chat_postMessage(
            channel=channel_id,
            text=f"Message received! You said: {text}"
        )

        return response

    logger.info(f"Ignored event for event_id: {event_id}")
    return jsonify({"status": "ignored"})

# Main Entry Point
if __name__ == "__main__":
    flask_app.run(port=3000)
