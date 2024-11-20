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
import os
import certifi
import logging
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

logging.basicConfig(level=logging.DEBUG)

# Set up SSL certificates
os.environ['SSL_CERT_FILE'] = certifi.where()
logging.info(f"Using SSL certificates from: {certifi.where()}")

# instantiating slack client
slack_client = WebClient(Config.SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(
    Config.SLACK_SIGNING_SECRET, "/slack/events", app
)
print(f"SlackEventAdapter initialized with signing secret: {Config.SLACK_SIGNING_SECRET}")
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

# @app.route("/slack/interactive-endpoint", methods=["POST"])
# def interactive_endpoint():
#     """
#     All interactive events like button click, input fields are received in this endpoint. We use this endpoint to handle the click event of 'Add task' button of create-task command.
#     :param:
#     :type:
#     :raise:
#     :return: Response object with 200 HTTP status
#     :rtype: Response
#     """
#     payload = json.loads(request.form.get("payload"))
#     print("payload:",payload)
#     try:
#         if payload["type"] == "block_actions":
#             actions = payload["actions"]
#             if len(actions) > 0:
#             # if actions:
#                 if actions[0]["action_id"] in ["create_action_button", "update_action_button"] :
#                     # Create Task or Update Task - button was clicked
#                     channel_id = payload["container"]["channel_id"]
#                     user_id = payload["user"]["id"]
#                     helper = ErrorHelper()
#                     ct = CreateTask()
#                     ut = UpdateTask(user_id=user_id)
#                     state_values = payload["state"]["values"]
#                     desc = None
#                     deadline = None
#                     points = None
#                     assignee = None
#                     for _, val in state_values.items():
#                         if "create_action_description" in val:
#                             desc = val["create_action_description"]["value"]
#                         elif "create_action_deadline" in val:
#                             deadline = val["create_action_deadline"]["selected_date"]
#                         elif "create_action_points" in val:
#                             if val["create_action_points"]["selected_option"] is not None:
#                                 points = val["create_action_points"]["selected_option"][
#                                     "value"
#                                 ]
#                             else:
#                                 points = None
#                         elif "create_action_assignees" in val: 
#                             if val["create_action_assignees"]["selected_option"] is not None: 
#                                 assignee = val["create_action_assignees"]["selected_option"]["value"] 
#                     if desc is None or deadline is None or points is None:
#                         error_blocks = helper.get_error_payload_blocks("createtask")
#                         slack_client.chat_postEphemeral(
#                             channel=channel_id, user=user_id, blocks=error_blocks
#                         )
#                     else:
#                         id = None
#                         if(actions[0]["action_id"] == "create_action_button"):
#                             blocks, id = ct.create_task(desc=desc, points=points, deadline=deadline, assignee=assignee, created_by=user_id)
#                             slack_client.chat_postEphemeral(
#                             channel=channel_id, user=user_id, blocks=blocks
#                             )
#                         else: 
#                             id = payload["actions"][0]["value"]
#                             blocks = ut.update_task(id=id, desc=desc, points=points, deadline=deadline, assignee=assignee)
#                             slack_client.chat_postEphemeral(
#                                 channel=channel_id, user=user_id, blocks=blocks
#                             )
#                         if(assignee): 
#                             assignerName = findName(user_id, channel_id)
                        
#                             message = "Task #" + str(id) + " has been assigned to you by " + assignerName
#                             slack_client.chat_postEphemeral(
#                                 channel=channel_id, user=assignee, blocks=[{"type": "section", "text": {"type": "plain_text", "text": message}}]
#                             )
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500                    
#     return make_response("", 200)
import random

@app.route("/slack/interactive-endpoint", methods=["POST"])
def interactive_endpoint():
    """
    Handles interactive events like button clicks for creating a task.
    """
    payload = json.loads(request.form.get("payload"))
    print("payload:", payload)

    try:
        if payload["type"] == "block_actions":
            actions = payload["actions"]
            if len(actions) > 0:
                if actions[0]["action_id"] == "create_action_button":
                    # Extract relevant info
                    channel_id = payload["container"]["channel_id"]
                    user_id = payload["user"]["id"]
                    user_name = payload["user"]["name"]  # Get the name of the user creating the task
                    state_values = payload["state"]["values"]
                    desc = None
                    deadline = None
                    points = None
                    assignee = None
                    
                    # Loop through state values to fetch task details
                    for _, val in state_values.items():
                        if "create_action_description" in val:
                            desc = val["create_action_description"]["value"]
                        elif "create_action_deadline" in val:
                            deadline = val["create_action_deadline"]["selected_date"]
                        elif "create_action_points" in val:
                            points = val["create_action_points"]["selected_option"]["value"] if val["create_action_points"]["selected_option"] else None
                        elif "create_action_assignees" in val:
                            assignee = val["create_action_assignees"]["selected_option"]["value"] if val["create_action_assignees"]["selected_option"] else None

                    # Check if necessary details are provided
                    if not desc or not deadline or not points:
                        error_blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "Please provide description, deadline, and points to create the task."}}]
                        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=error_blocks)
                    else:
                        # Generate a random task ID
                        task_id = random.randint(10000, 99999)  # Random task ID between 10000 and 99999
                        message = f"Task created successfully!\n*Description:* {desc}\n*Points:* {points}\n*Deadline:* {deadline}\n*Task ID:* {task_id}"

                        # Post success message to the user who created the task
                        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, text=message)

                        # If there's an assignee, fetch their name and notify them with the task ID and assigner's name
                        # Ensure the assignee is being correctly fetched from the Slack API
                    if assignee:
                        # Debugging: Log assignee ID to verify it's being passed correctly
                        print(f"Assignee ID: {assignee}")

                        # Fetch assignee's information from Slack API
                        assignee_info = slack_client.users_info(user=assignee)

                        # Debugging: Log assignee info to ensure response is correct
                        print(f"Assignee Info: {assignee_info}")

                        if assignee_info.get('ok', False):
                            # Get the display name of the assignee
                            assignee_display_name = assignee_info["user"]["profile"].get("display_name", "No display name")
                            print(f"Assignee Display Name: {assignee_display_name}")

                            # Prepare the message for the assignee
                            assignee_message = f"Task #{task_id} has been assigned to you by {user_name}."
        
                            # Send the message to the assignee
                            slack_client.chat_postEphemeral(channel=channel_id, user=assignee, text=assignee_message)
                        else:
                            print(f"Error: Unable to fetch assignee information for user ID: {assignee}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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


@app.route("//co", methods=["POST"])
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
    if(text == "me"):
        vt = ViewMyTasks(user_id) 
        payload = vt.get_list()
    elif(text == "today"): 
        vdt = ViewDeadlineTasks()
        payload = vdt.get_list()
    elif(len(text) == 0):
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
    # print(f"Channel ID: {channel_id}, User ID: {user_id}, Blocks: {blocks}")
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    # print(channel_id)
    try:
        ct = CreateTask(getUsers(channel_id))
        blocks = ct.create_task_input_blocks()
        slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # return Response(), 200
    # data = request.form
    # channel_id = data.get("channel_id")
    # user_id = data.get("user_id")

    # try:
    #     slack_client.chat_postEphemeral(
    #         channel=channel_id,
    #         user=user_id,
    #         text="Testing /create endpoint! 🚀 and channel id is "+channel_id+"user id is "+user_id
    #     )
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

    return Response(), 200

@app.route("/user", methods=["POST"])
def get_user_id():
    """
    Endpoint to respond to the /user Slack slash command.
    Fetches and returns the user's Slack ID.
    """
    # Extract the user ID from the Slack request payload
    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")

    if not user_id:
        return jsonify({"error": "User ID not found in the request"}), 400

    # Respond with the user ID and name
    return jsonify({
        "response_type": "ephemeral",  # Makes the response visible only to the user
        "text": f"Your Slack User ID: `{user_id}`\nYour Slack Username: `{user_name}`"
    }), 200

@app.route("/test-help", methods=["GET"])
def test_help():
    return jsonify({"message": "Test Help Endpoint"})
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message":"Hello World!"})


@app.route("/updatetask", methods=["POST"])
def update(): 
    """
    Endpoint to update a task, this endpoint triggers an ephemeral message for the user to edit task details.
    """
    try:
        data = request.form
        channel_id = data.get("channel_id")
        user_id = data.get("user_id")

        app.logger.info(f"Received update request: channel_id={channel_id}, user_id={user_id}")

        # Create UpdateTask object
        ut = UpdateTask(user_id, data, getUsers(channel_id))

        # Check if task exists
        taskExists = ut.checkTaskID()
        if taskExists:
            blocks = ut.create_task_input_blocks()

            # Send the ephemeral message
            response = slack_client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks)
            if response.get("ok"):
                app.logger.info("Ephemeral message sent successfully.")
                return jsonify({"status": "success", "message": "Task update initiated"}), 200
            else:
                app.logger.error(f"Error sending ephemeral message: {response}")
                return jsonify({"status": "error", "message": "Failed to send message"}), 500
        else:
            app.logger.error("Task ID not found.")
            return jsonify({"status": "error", "message": "Task ID not found"}), 404
    except Exception as e:
        app.logger.error(f"Exception occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

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
    print("Request Headers: ", request.headers)

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
