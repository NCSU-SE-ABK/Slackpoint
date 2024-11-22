from copy import deepcopy
import random
from models import *
from helpers.errorhelper import ErrorHelper
import datetime

class UpdateTask: 
    """ 
    This class handles the Update Task functionality. 
    """

    base_create_task_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">{greeting}! Your task SP-{id} was updated successfully.",
        },
    }

    greetings = ["Awesome", "Great", "Congratulations", "Well done", "Let's go"]

    def __init__(self, user_id="", data=[], users=[]):
        """
        Constructor to initialize payload object

        :param user_id: Slack user ID
        :param data: Task data
        :param users: List of users for the task
        :return: None
        """
        self.payload = {
            "response_type": "ephemeral", 
            "blocks": []
        }
        self.user_id = db.session.query(User).filter_by(slack_user_id=user_id).first().user_id
        self.data = data
        self.users = users

    def checkTaskID(self): 
        helper = ErrorHelper()
        self.current_task_id = int(self.data.get('text'))

        # Check if task id exists
        exists = db.session.query(db.exists().where(Task.task_id == self.current_task_id)).scalar()
        if exists: 
            return True
        else: 
            helper.get_command_help("no_task_id")

    def create_task_input_blocks(self):
        """
        Create blocks list containing input fields for description, deadline, points of a task, along with a button to update the task
        Ensure that the fields are pre-populated with the values that already exist in the database

        :return: Blocks list
        """
        task = db.session.query(Task).filter_by(task_id=self.current_task_id).first()
        description = str(task.description)
        deadline = str(task.deadline.strftime("%Y-%m-%d"))
        points = str(task.points)

        user_id = db.session.query(Assignment).filter_by(assignment_id=self.current_task_id).first()
        if user_id: 
            slack_user_id = db.session.query(User).filter_by(user_id=user_id.user_id).first().slack_user_id

        block_task_id = {
            "type": "header", 
            "text": {
                "type": "plain_text", 
                "text": "Task " + str(self.current_task_id) + ": ", 
            }, 
        }

        block_description = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_description",
                "initial_value": description,
            },
            "label": {"type": "plain_text", "text": "Description", "emoji": True},
        }
        block_deadline = {
            "type": "input",
            "element": {
                "type": "datepicker",
                "initial_date": deadline,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True,
                },
                "action_id": "create_action_deadline",
            },
            "label": {"type": "plain_text", "text": "Deadline", "emoji": True},
        }
        block_points = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select", "emoji": True},
                "options": [
                    {"text": {"type": "plain_text", "text": "1", "emoji": False}, "value": "1"},
                    {"text": {"type": "plain_text", "text": "2", "emoji": False}, "value": "2"},
                    {"text": {"type": "plain_text", "text": "3", "emoji": False}, "value": "3"},
                    {"text": {"type": "plain_text", "text": "4", "emoji": False}, "value": "4"},
                    {"text": {"type": "plain_text", "text": "5", "emoji": False}, "value": "5"},
                ],
                "initial_option": {
                    "text": {"type": "plain_text", "text": points, "emoji": False},
                    "value": points,
                },
                "action_id": "create_action_points",
            },
            "label": {"type": "plain_text", "text": "Points", "emoji": True},
        }
        block_users = {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select", "emoji": True},
                "options": [],
                "action_id": "create_action_assignees",
            },
            "label": {"type": "plain_text", "text": "Assignees", "emoji": True},
        }

        selectedUser = {}
        for user in self.users: 
            placeholder =  {"text": {"type": "plain_text", "emoji": False}}
            placeholder["text"]["text"] = user["name"]
            placeholder["value"] = user["user_id"]
            if user["user_id"] == slack_user_id: 
                selectedUser = placeholder
            block_users["element"]["options"].append(placeholder)

        block_users["element"]["initial_option"] = selectedUser

        block_actions_button = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Update task"},
            "action_id": "update_action_button",
            "value": str(self.current_task_id)
        }
        block_actions = {"type": "actions", "elements": [block_actions_button]}

        blocks = [block_task_id, block_description, block_deadline, block_points, block_users, block_actions]
        return blocks

    def update_task(self, id, desc, points, deadline, assignee):
        """
        Update a task in database and returns payload with success message.

        :param desc: Description of task
        :param points: Points of task
        :param deadline: Deadline of task
        :param assignee: Assignee Slack user ID
        :return: Blocks list of response payload
        """
        response = deepcopy(self.base_create_task_block_format)

        creatorUserId = db.session.query(Task).filter_by(task_id=id).first().created_by
        sameUser = (creatorUserId == self.user_id)
        if not sameUser: 
            response["text"]["text"] = "You are not allowed to make changes to this task."
            return response

        # Check if the assignee exists
        exists = db.session.query(db.exists().where(User.slack_user_id == assignee)).scalar()
        if not exists: 
            user = User(slack_user_id=assignee)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)    

        # Get user ID for the assignee
        user_id = db.session.query(User).filter_by(slack_user_id=assignee).first().user_id

        try:
            # Update the task
            db.session.query(Task).filter_by(task_id=id).update(dict(description=desc, points=points, deadline=deadline))  
            db.session.query(Assignment).filter_by(assignment_id=id).update(dict(user_id=user_id))
            db.session.commit()

            # Prepare success response
            response["text"]["text"] = response["text"]["text"].format(greeting=random.choice(self.greetings), id=id)
        except Exception as e:
            db.session.rollback()
            response["text"]["text"] = f"Error: {str(e)}"
        
        self.payload["blocks"].append(response)
        return self.payload["blocks"]
