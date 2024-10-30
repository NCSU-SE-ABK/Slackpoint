from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from flask import Flask, make_response, request, jsonify, Response
import json
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
from commands.dailystandupreport import DailyStandupReport

import ssl
import certifi

from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)


# Initialize Slack client
ssl_context = ssl.create_default_context(cafile=certifi.where())
slack_client = WebClient(Config.SLACK_BOT_TOKEN, ssl=ssl_context)
slack_events_adapter = SlackEventAdapter(
    Config.SLACK_SIGNING_SECRET, "/slack/events", app
)

def getUsers(channel_id):
    """
    Retrieves a list of users from a specific Slack channel.

    :param channel_id: ID of the Slack channel.
    :type channel_id: str
    :return: List of users in the channel.
    :rtype: list[dict]

    **Why**: Essential for retrieving all members to assign or manage tasks within a specific channel.
    **How**: Usage within task-related endpoints to gather or assign channel users.
    """
    users = []
    result = slack_client.conversations_members(channel=channel_id)
    for user in result['members']:
        info = slack_client.users_info(user=user).data
        if 'real_name' in info['user'].keys():
            if info['user']['real_name'] != 'bot':
                users.append({"name": info['user']['real_name'], "user_id": info['user']['id']})
    return users

def findName(slack_id, channel_id):
    """
    Finds a user's name in a Slack channel by their Slack ID.

    :param slack_id: Slack ID of the user.
    :type slack_id: str
    :param channel_id: ID of the Slack channel.
    :type channel_id: str
    :return: Name of the user.
    :rtype: str

    **Why**: Used to retrieve the actual name of a user for task assignments or updates, enhancing response clarity.
    """
    for element in getUsers(channel_id):
        if element['user_id'] == slack_id:
            return element['name']

@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    """
    Endpoint to handle interactive Slack events like button clicks, such as for creating or updating tasks.

    :return: Response object with 200 HTTP status.
    :rtype: Response

    **Why**: Allows the bot to handle interactive elements and input fields, providing a more dynamic user experience.
    """
    payload = json.loads(request.form.get("payload"))
    if payload["type"] == "block_actions":
        actions = payload["actions"]
        if len(actions) > 0:
            if actions[0]["action_id"] in ["create_action_button", "update_action_button"]:
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ct = CreateTask()
                ut = UpdateTask(user_id=user_id)
                state_values = payload["state"]["values"]
                desc, deadline, points, assignee = None, None, None, None

                for _, val in state_values.items():
                    if "create_action_description" in val:
                        desc = val["create_action_description"]["value"]
                    elif "create_action_deadline" in val:
                        deadline = val["create_action_deadline"]["selected_date"]
                    elif "create_action_points" in val:
                        points = val["create_action_points"]["selected_option"]["value"] if val["create_action_points"]["selected_option"] else None
                    elif "create_action_assignees" in val:
                        assignee = val["create_action_assignees"]["selected_option"]["value"] if val["create_action_assignees"]["selected_option"] else None

                if desc is None or deadline is None or points is None:
                    error_blocks = helper.get_error_payload_blocks("createtask")
                    slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=error_blocks)
                else:
                    id = None
                    if actions[0]["action_id"] == "create_action_button":
                        blocks, id = ct.create_task(desc=desc, points=points, deadline=deadline, assignee=assignee, created_by=user_id)
                        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
                    else:
                        id = payload["actions"][0]["value"]
                        blocks = ut.update_task(id=id, desc=desc, points=points, deadline=deadline, assignee=assignee)
                        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)

                    if assignee:
                        assignerName = findName(user_id, channel_id)
                        message = f"Task #{id} has been assigned to you by {assignerName}"
                        slack_client.chat_postEphemeral(channel=channel_id, user=assignee, blocks=[{"type": "section", "text": {"type": "plain_text", "text": message}}])

    return make_response("", 200)


@app.route("/")
def basic():
    """
    Health check endpoint.

    :return: 'Hello World' - the official health check response text.
    :rtype: str

    **Why**: Ensures the server is running and accessible.
    """
    return "Hello World"


@app.route("/viewpending", methods=["POST"])
def vpending():
    """
    Endpoint to view the pending tasks based on the requester's filters.

    :return: Response object with payload containing pending tasks.
    :rtype: Response

    **Why**: Provides users with an organized view of pending tasks, allowing them to check tasks assigned to them,
    tasks due today, or all uncompleted tasks.
    """
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")

    payload = None
    if text == "me":
        vt = ViewMyTasks(user_id)
        payload = vt.get_list()
    elif text == "today":
        vdt = ViewDeadlineTasks()
        payload = vdt.get_list()
    elif len(text) == 0:
        vp = ViewPoints(progress=0.0)
        payload = vp.get_list()

    return jsonify(payload)


@app.route("/viewcompleted", methods=["POST"])
def vcompleted():
    """
    Endpoint to view completed tasks.

    :return: Response object with payload containing completed tasks.
    :rtype: Response

    **Why**: Allows users to view completed tasks for tracking and reporting purposes.
    """
    data = request.form
    vp = ViewPoints(progress=1.0)
    payload = vp.get_list()
    return jsonify(payload)


@app.route("/taskdone", methods=["POST"])
def taskdone():
    """
    Endpoint to mark a task as completed.

    :return: Response object with payload containing task completion message.
    :rtype: Response

    **Why**: Enables users to update task status, marking it as completed.
    """
    data = request.form
    td = TaskDone(data)
    payload = td.update_points()
    return jsonify(payload)


@app.route("/create", methods=["POST"])
def create():
    """
    Endpoint to create a new task. Triggers an ephemeral message for user input.

    :return: Response object with 200 HTTP status.
    :rtype: Response

    **Why**: Provides an interactive way for users to create tasks, with a structured form for details.
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
    Endpoint to update an existing task, triggering a pre-filled form for user edits.

    :return: Response object with 200 HTTP status.
    :rtype: Response

    **Why**: Allows users to easily modify tasks, using a form pre-populated with existing task details.
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
    Helper endpoint to view all commands and their usage.

    :return: Response object with payload containing command descriptions.
    :rtype: Response

    **Why**: Provides guidance to users on available commands and how to use them.
    """
    h = Help()
    payload = h.help_all()
    return jsonify(payload)


@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    """
    Endpoint to view the leaderboard for top users.

    :return: Response object with payload containing leaderboard details.
    :rtype: Response

    **Why**: Encourages user engagement by showcasing top-performing users.
    """
    l = Leaderboard()
    payload = l.view_leaderboard()
    return jsonify(payload)


print("Starting standup report schedule")
with app.app_context():
    # update the channel ID with the channel ID you want to post the daily standup report to
    slack_client.conversations_join(channel='C07T6TACHJA')
    daily_report = DailyStandupReport(app, "C07T6TACHJA")
    daily_report.schedule_daily_report(report_time="15:59")

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
