import time
import requests
import json
import logging
from flask import Flask
from threading import Thread

# Configuration Section
SLACK_WEBHOOK_URL = ""
SLACK_BOT_TOKEN = ""
CHANNEL_ID = ""
SLACK_API_URL = ""

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Flask Application Initialization
app = Flask(__name__)

# Store last message timestamp to prevent duplicate processing
last_timestamp = None

def fetch_messages():
    """
    Poll Slack channel for the latest message and respond if it's new.
    """
    global last_timestamp
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"channel": CHANNEL_ID, "limit": 1}

    try:
        response = requests.get(SLACK_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if "messages" in data and data["messages"]:
            latest_message = data["messages"][0]
            timestamp = latest_message.get("ts")
            text = latest_message.get("text")
            user = latest_message.get("user")

            if timestamp and text and timestamp != last_timestamp:
                last_timestamp = timestamp
                logger.info(f"Received message from user {user}: {text}")
                send_slack_message("I received your message!")

    except requests.RequestException as e:
        logger.error(f"Error fetching messages from Slack: {e}")

def send_slack_message(message: str):
    """
    Send a message to Slack via the incoming webhook.
    Args:
        message (str): The message to send.
    """
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        logger.info("Message sent successfully via webhook.")

    except requests.RequestException as e:
        logger.error(f"Failed to send message to Slack: {e}")

def start_polling():
    """
    Background thread function to continuously poll Slack for new messages.
    """
    while True:
        fetch_messages()
        time.sleep(3)  # Wait before polling again

if __name__ == "__main__":
    # Start background polling thread
    Thread(target=start_polling, daemon=True).start()

    # Run Flask application
    app.run(port=3000)
