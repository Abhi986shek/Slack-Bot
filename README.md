# Slack Bots - Flask Integration

This repository contains three different Slack bot implementations using Flask and the Slack API. These bots interact with Slack in different ways: handling events via HTTP requests, socket mode, and via incoming webhooks.

## Projects Overview

1. **`http_slack_bot.py`**
   A Slack bot using Flask that listens for incoming HTTP requests, handles events like messages, and responds using Slack's REST API.

2. **`socket_slack_bot.py`**
   A Slack bot using Flask and Socket Mode to handle Slack events like reactions, messages, and other real-time interactions.

3. **`webhook_slack_bot.py`**
   A Slack bot using Flask that periodically fetches messages from a Slack channel via the Slack API and responds using an incoming webhook.



## Prerequisites

Before running any of these bots, you will need to have the following installed:

* Python 3.x
* Flask (`pip install Flask`)
* Slack SDK for Python (`pip install slack_bolt`)
* Requests library (`pip install requests`)

Additionally, you'll need the following Slack API tokens and keys:

* **Bot Token**: You can generate this in the Slack App's OAuth & Permissions section.
* **App-Level Token**: Required for Slack’s Socket Mode.
* **Webhook URL**: Used for sending responses to Slack via a webhook.



## Bot Setup

### 1. **`http_slack_bot.py`** (HTTP-based Slack Bot)

This bot listens for events from Slack via HTTP endpoints and responds accordingly.

* **Dependencies**: `Flask`, `slack_bolt`
* **Setup**:

  * Set up your Slack App's Bot Token and Signing Secret.
  * Make sure your app is configured with the correct Event Subscriptions for Slack to send events to your endpoint.



### 2. **`socket_slack_bot.py`** (Socket Mode Slack Bot)

This bot uses Slack's Socket Mode to handle events like message reactions and messages in real-time.

* **Dependencies**: `Flask`, `slack_bolt`
* **Setup**:

  * Set up the `APP_LEVEL_TOKEN` and `BOT_TOKEN` for your Slack App.
  * Ensure your Slack App has the necessary permissions to listen for message events and reaction events.



### 3. **`webhook_slack_bot.py`** (Webhook-based Slack Bot)

This bot fetches new messages from Slack periodically and responds using Slack's incoming webhook.

* **Dependencies**: `Flask`, `requests`
* **Setup**:

  * Set up your Slack Bot Token and Incoming Webhook URL.
  * Ensure your bot has access to the channel you want to monitor.



## Key Features

* **`http_slack_bot.py`**:

  * Handles Slack events like messages sent to channels.
  * Responds immediately when a message is received via the HTTP endpoint.
* **`socket_slack_bot.py`**:

  * Handles events like message reactions using Slack's real-time Socket Mode.
  * Responds based on reactions, such as thumbs up (+1) or thumbs down (-1).
* **`webhook_slack_bot.py`**:

  * Polls Slack for new messages at regular intervals.
  * Uses an incoming webhook to send replies.

---

## Logging

All bots use logging to capture events and errors. Ensure that the appropriate logging configuration is in place for debugging and troubleshooting. Replace `print` statements with logging in the code for better traceability.

---
