"""
Slack Bot using Socket Mode

This script uses Slack Bolt for Python to implement a Slack bot that operates in Socket Mode.
It listens for message events and reaction_added events, responding with context-aware messages.
"""

from slack_bolt import App  # type: ignore
from slack_bolt.adapter.socket_mode import SocketModeHandler  # type: ignore
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack credentials (should ideally be loaded from environment variables or a config file)
APP_LEVEL_TOKEN = ""  # App-Level Token
BOT_TOKEN = ""  # Bot Token

# Initialize Slack Bolt App
app = App(token=BOT_TOKEN)


@app.event("message")
def handle_message(event, say, logger):
    """
    Handles incoming Slack messages.

    Parameters:
    - event (dict): The incoming event payload
    - say (function): Function to send a message in the same channel
    - logger (Logger): The logger instance
    """
    logger.info(f"Received message event: {event}")
    say("I received your message!")


@app.event("reaction_added")
def handle_reaction(event, client, logger):
    """
    Handles reactions added to messages in Slack.

    Parameters:
    - event (dict): The incoming event payload
    - client (WebClient): Slack Web API client
    - logger (Logger): The logger instance
    """
    logger.info(f"Received reaction event: {event}")

    reaction = event.get("reaction")
    item = event.get("item", {})
    channel = item.get("channel")
    message_ts = item.get("ts")

    # Determine the response message based on the reaction
    if reaction == "+1":
        response_text = "You liked it! 👍"
    elif reaction == "-1":
        response_text = "You disliked it! 👎"
    else:
        response_text = f"You reacted with :{reaction}:"

    if channel and response_text:
        client.chat_postMessage(
            channel=channel,
            text=response_text,
            # Uncomment below to thread response under the original message
            # thread_ts=message_ts
        )


if __name__ == "__main__":
    # Start the app in Socket Mode
    handler = SocketModeHandler(app, APP_LEVEL_TOKEN)
    logger.info("Starting Slack bot in Socket Mode...")
    handler.start()
