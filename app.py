from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from flask import Flask, make_response, request, jsonify, Response
import json
from slack.errors import SlackApiError
from datetime import datetime, timedelta
import threading
import time
import datetime

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
from commands.requesthelp import RequestHelp
from commands.dailystandupreport import DailyStandupReport

import ssl
import certifi

from models import *

# List to store reminders
reminders = []

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# instantiating slack client
ssl_context = ssl.create_default_context(cafile=certifi.where())
slack_client = WebClient(Config.SLACK_BOT_TOKEN, ssl=ssl_context)
slack_events_adapter = SlackEventAdapter(
    Config.SLACK_SIGNING_SECRET, "/slack/events", app
)


def getUsers(channel_id):
    users = []
    result = slack_client.conversations_members(channel=channel_id)
    for user in result['members']:
        info = slack_client.users_info(user = user).data
        if 'real_name' in info['user'].keys(): 
            if(info['user']['real_name'] != 'bot'):
                users.append({"name": info['user']['real_name'], "user_id": info['user']['id'], "username": info['user']['name']})
    return users


def findName(slack_id, channel_id):
    for element in getUsers(channel_id):
        if element['user_id'] == slack_id:
            return element['name']


@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    """
     All interactive events like button click, input fields are received in this endpoint. We use this endpoint to handle the click event of 'Add task' button of create-task command.
     :param:
     :type:
     :raise:
     :return: Response object with 200 HTTP status
     :rtype: Response
     """
    payload = json.loads(request.form.get("payload"))
    if payload["type"] == "block_actions":
        actions = payload["actions"]
        if len(actions) > 0:
            if actions[0]["action_id"] in ["create_action_button", "update_action_button"]:
                # Create Task or Update Task - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ct = CreateTask()
                ut = UpdateTask(user_id=user_id)
                state_values = payload["state"]["values"]
                desc = None
                deadline = None
                points = None
                assignee = None
                for _, val in state_values.items():
                    if "create_action_description" in val:
                        desc = val["create_action_description"]["value"]
                    elif "create_action_deadline" in val:
                        deadline = val["create_action_deadline"]["selected_date"]
                    elif "create_action_points" in val:
                        if val["create_action_points"]["selected_option"] is not None:
                            points = val["create_action_points"]["selected_option"][
                                "value"
                            ]
                        else:
                            points = None
                    elif "create_action_assignees" in val:
                        if val["create_action_assignees"]["selected_option"] is not None:
                            assignee = val["create_action_assignees"]["selected_option"]["value"]
                if desc is None or deadline is None or points is None:
                    error_blocks = helper.get_error_payload_blocks("createtask")
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=error_blocks
                    )
                else:
                    id = None
                    if (actions[0]["action_id"] == "create_action_button"):
                        blocks, id = ct.create_task(desc=desc, points=points, deadline=deadline, assignee=assignee,
                                                    created_by=user_id)
                        slack_client.chat_postEphemeral(
                            channel=channel_id, user=user_id, blocks=blocks
                        )
                    else:
                        id = payload["actions"][0]["value"]
                        blocks = ut.update_task(id=id, desc=desc, points=points, deadline=deadline, assignee=assignee)
                        slack_client.chat_postEphemeral(
                            channel=channel_id, user=user_id, blocks=blocks
                        )
                    if (assignee):
                        assignerName = findName(user_id, channel_id)

                        message = "Task #" + str(id) + " has been assigned to you by " + assignerName
                        slack_client.chat_postEphemeral(
                            channel=channel_id, user=assignee,
                            blocks=[{"type": "section", "text": {"type": "plain_text", "text": message}}]
                        )
            elif actions[0]["action_id"] == "submit_reminder":
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
    """
    Endpoint to set a reminder for a user. This endpoint triggers an interactive message
    for the user to enter the date, time, message, and select a task for the reminder.

    :param: None
    :type: None
    :raise: None
    :return: Response object with status of the reminder setup
    :rtype: Response
    """
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

@app.route("/requesthelp", methods=["POST"])
def request_help():
    """
    Endpoint to request help on a task.

    :return: JSON response with confirmation or error message.
    :rtype: Response
    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    # Assume teammates are retrieved with their Slack IDs and names
    teammates = getUsers(channel_id)

    rh = RequestHelp(app, data, teammates=teammates)
    payload = rh.request_help()

    return jsonify(payload)

print("Starting standup report schedule")
with app.app_context():
    slack_client.conversations_join(channel='C07T6TACHJA')
    daily_report = DailyStandupReport(app, "C07T6TACHJA")
    daily_report.schedule_daily_report(report_time="15:59")


# Function to send the reminder message
def send_reminder(channel_id, message, task_id):
    """
    Function to send a reminder message to a specified Slack channel.

    :param channel_id: The ID of the Slack channel where the reminder will be sent.
    :type channel_id: str
    :param message: The reminder message to be sent.
    :type message: str
    :param task_id: The ID of the task associated with the reminder.
    :type task_id: str
    :raise: SlackApiError if there is an error sending the message.
    :return: None
    """
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
    """
    Function to get the ID of a Slack channel given its name.

    :param channel_name: The name of the Slack channel.
    :type channel_name: str
    :raise: SlackApiError if there is an error fetching the channels.
    :return: The ID of the Slack channel if found, otherwise None.
    :rtype: str or None
    """
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
    """
    Background worker function to check and send reminders at the scheduled time.

    This function runs in an infinite loop, checking the current time against the
    scheduled reminder times. If a reminder's time is due, it sends the reminder
    message to the specified Slack channel and removes the reminder from the list.

    :param: None
    :type: None
    :raise: None
    :return: None
    """
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
