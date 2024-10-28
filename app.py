from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from flask import Flask, make_response, request, jsonify, Response
import json
import psycopg2
from slack.errors import SlackApiError
from datetime import datetime, timedelta
import threading
import time

from commands.help import Help
from models import db
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from commands.viewpoints import ViewPoints
from configuration.env_config import Config
from commands.createtask import CreateTask
from helpers.errorhelper import ErrorHelper
from commands.updatetask import UpdateTask
from commands.viewmytasks import ViewMyTasks
from commands.viewdeadlinetasks import ViewDeadlineTasks

# List to store reminders
reminders = []

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# instantiating slack client
slack_client = WebClient(Config.SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(
    Config.SLACK_SIGNING_SECRET, "/slack/events", app
)


def getUsers(channel_id):
    users = []
    result = slack_client.conversations_members(channel=channel_id)
    for user in result['members']:
        info = slack_client.users_info(user=user).data
        if 'real_name' in info['user'].keys():
            if info['user']['real_name'] != "bot":
                users.append({"name": info['user']['real_name'], "user_id": info['user']['id']})
    return users


def findName(slack_id, channel_id):
    for element in getUsers(channel_id):
        if element['user_id'] == slack_id:
            return element['name']


@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    payload = json.loads(request.form.get("payload"))
    if payload["type"] == "block_actions":
        actions = payload["actions"]
        if len(actions) > 0:
            if actions[0]["action_id"] == "submit_reminder":
                selected_date = payload["state"]["values"]["reminder_date"]["select_date"]["selected_date"]
                selected_time = payload["state"]["values"]["reminder_time"]["select_time"]["selected_time"]
                reminder_message = payload["state"]["values"]["reminder_message"]["message_input"]["value"]
                selected_task = payload["state"]["values"]["reminder_task"]["select_task"]["selected_option"]["value"]
                channel_id = payload["channel"]["id"]

                reminder_datetime = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")

                reminders.append({
                    "channel": channel_id,
                    "message": reminder_message,
                    "time": reminder_datetime,
                    "task_id": selected_task
                })

                response = {
                    "replace_original": True,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {"type": "plain_text", "text": "✅ Reminder Scheduled!"}
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Message:* {reminder_message}\n*Scheduled For:* {reminder_datetime.strftime('%A, %B %d at %I:%M %p')}\n*Task ID:* {selected_task}"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": ":bell: You'll receive a reminder in the specified channel at the scheduled time."
                                }
                            ]
                        }
                    ]
                }

    return make_response("", 200)

@app.route("/")
def basic():
    """
    Health check endpoint

    :param:
    :type:
    :raise:
    :return: 'Hello World' - the official health check response text
    :rtype: str

    """
    return "Hello World"


@app.route("/viewpending", methods=["POST"])
def vpending():
    """
    Endpoint to view the pending tasks

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of pending tasks
    :rtype: Response

    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    payload = None
    if (text == "me"):
        vt = ViewMyTasks(user_id)
        payload = vt.get_list()
    elif (text == "today"):
        vdt = ViewDeadlineTasks()
        payload = vdt.get_list()
    elif (len(text) == 0):
        vp = ViewPoints(progress=0.0)
        payload = vp.get_list()

    return jsonify(payload)


@app.route("/viewcompleted", methods=["POST"])
def vcompleted():
    """
    Endpoint to view the completed tasks

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of completed tasks
    :rtype: Response

    """

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    vp = ViewPoints(progress=1.0)
    payload = vp.get_list()

    return jsonify(payload)


@app.route("/taskdone", methods=["POST"])
def taskdone():
    """
    Endpoint to mark a task as completed

    :param:
    :type:
    :raise:
    :return: Response object with payload containing task completion message
    :rtype: Response

    """

    data = request.form
    td = TaskDone(data)
    payload = td.update_points()
    return jsonify(payload)


@app.route("/reminder", methods=["POST"])
def reminder():
    channel_id = request.form.get("channel_id")
    user_id = request.form.get("user_id")
    print("User ID", user_id)

    # Fetch pending tasks for the user
    vt = ViewMyTasks(user_id)
    pending_tasks = vt.get_list()["blocks"]
    print("Pending tasks", pending_tasks)

    task_options = [
            {
                "text": {"type": "plain_text", "text": task["text"]["text"]},
                "value": task["text"]["text"].split(" ")[0].strip()
            }
            for task in pending_tasks
        ]
    # Ensure pending_tasks is a list of dictionaries

    # Check if task_options is empty and handle it
    if not task_options:
        task_options = [
            {
                "text": {"type": "plain_text", "text": "No pending tasks available"},
                "value": "no_task"
            }
        ]

    # Send interactive message to capture date, time, message, and task
    slack_client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Please select the date, time, message, and task for your reminder."}
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "reminder_date",
                "element": {
                    "type": "datepicker",
                    "action_id": "select_date",
                    "placeholder": {"type": "plain_text", "text": "Select a date"}
                },
                "label": {"type": "plain_text", "text": "Date"}
            },
            {
                "type": "input",
                "block_id": "reminder_time",
                "element": {
                    "type": "timepicker",
                    "action_id": "select_time",
                    "placeholder": {"type": "plain_text", "text": "Select a time"}
                },
                "label": {"type": "plain_text", "text": "Time"}
            },
            {
                "type": "input",
                "block_id": "reminder_message",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "message_input",
                    "placeholder": {"type": "plain_text", "text": "Enter reminder message"}
                },
                "label": {"type": "plain_text", "text": "Message"}
            },
            {
                "type": "input",
                "block_id": "reminder_task",
                "element": {
                    "type": "static_select",
                    "action_id": "select_task",
                    "placeholder": {"type": "plain_text", "text": "Select a task"},
                    "options": task_options
                },
                "label": {"type": "plain_text", "text": "Task"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Set Reminder"},
                        "action_id": "submit_reminder"
                    }
                ]
            }
        ],
        text="Schedule a reminder",
    )

    return jsonify({"status": "success"}), 200

@app.route("/create", methods=["POST"])
def create():
    """
    Endpoint to create a new task, this endpoint triggers an ephemeral message for the user to enter task details for creation

    :param:
    :type:
    :raise:
    :return: Response object with 200 HTTP status
    :rtype: Response

    """

    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")

    ct = CreateTask(getUsers(channel_id))
    blocks = ct.create_task_input_blocks()

    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/updatetask", methods=["POST"])
def update():
    """
    Endpoint to update a task, this endpoint triggers an ephemeral message for the user to edit task details for updation
    The form will be prepopulated with the values that were entered during the task creation/previous task updation
    :param:
    :type:
    :raise:
    :return: Response object with 200 HTTP status
    :rtype: Response
    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    ut = UpdateTask(user_id, data, getUsers(channel_id))
    taskExists = ut.checkTaskID()
    if taskExists:
        blocks = ut.create_task_input_blocks()
        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    return Response(), 200


@app.route("/help", methods=["POST"])
def help():
    """
    A helper endpoint to view all commands and how to use them

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of all commands and how to use them
    :rtype: Response

    """

    h = Help()
    payload = h.help_all()
    return jsonify(payload)


@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    """
    Endpoint to view the leaderboard

    :param:
    :type:
    :raise:
    :return: Response object with payload object containing details of champions leading the SlackPoint challenge
    :rtype: Response

    """

    l = Leaderboard()
    payload = l.view_leaderboard()
    return jsonify(payload)



# Function to send the reminder message
def send_reminder(channel_id, message, task_id):
    try:
        response = slack_client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "⏰ Reminder Notification",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🔔 Reminder:* {message}\n*Task ID:* {task_id}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": ":bell: This is your scheduled reminder. Stay on top of your tasks!"
                        }
                    ]
                }
            ]
        )
        print(f"Message sent to {channel_id}: {message}")
    except SlackApiError as e:
        print(f"Error sending reminder: {e.response['error']}")


def get_channel_id(channel_name):
    try:
        response = slack_client.conversations_list()
        channels = response['channels']
        for channel in channels:
            if channel['name'] == channel_name.strip("#"):  # Remove '#' if present
                return channel['id']
    except SlackApiError as e:
        print(f"Error fetching channels: {e.response['error']}")
    return None


# Background thread to check and send reminders
def reminder_worker():
    while True:
        now = datetime.now()
        for reminder in reminders[:]:
            if reminder["time"] <= now:
                send_reminder(reminder["channel"], reminder["message"], reminder["task_id"])
                reminders.remove(reminder)
        time.sleep(1)


# Start the background worker
threading.Thread(target=reminder_worker, daemon=True).start()

print("Starting the server 1")
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
