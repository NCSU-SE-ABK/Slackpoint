from commands.taskdone import TaskDone
from commands.leaderboard import Leaderboard
from flask import Flask, make_response, request, jsonify, Response
import json
import psycopg2
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
    result = slack_client.conversations_members(channel= channel_id)
    for user in result['members']:
        info = slack_client.users_info(user = user).data
        if 'real_name' in info['user'].keys(): 
            if(info['user']['real_name'] != 'bot'):
                users.append({"name": info['user']['real_name'], "user_id": info['user']['id']})
    return users

def findName(slack_id, channel_id): 
    for element in getUsers(channel_id): 
        if(element['user_id'] == slack_id): 
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
            if actions[0]["action_id"] == "create_action_button":
                # Create Task - button was clicked
                channel_id = payload["container"]["channel_id"]
                user_id = payload["user"]["id"]
                helper = ErrorHelper()
                ct = CreateTask()
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
                    blocks = ct.create_task(desc=desc, points=points, deadline=deadline, assignee=assignee)
                    slack_client.chat_postEphemeral(
                        channel=channel_id, user=user_id, blocks=blocks
                    )
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


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
