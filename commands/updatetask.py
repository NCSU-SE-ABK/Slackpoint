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

        :param:
        :type:
        :raise:
        :return: None
        :rtype: None

        """
        self.payload = {
            "response_type": "ephemeral", 
            "blocks": []
        }
        self.user_id = user_id
        self.data = data
        self.users = users

    def checkTaskID(self): 
        helper = ErrorHelper()
        self.current_task_id = int(self.data.get('text'))

        # check if task id exists
        exists = db.session.query(db.exists().where(Task.task_id == self.current_task_id)).scalar()

        if exists: 
            return True

        else: 
            helper.get_command_help("no_task_id")
    def create_task_input_blocks(self):
        """
        Create blocks list containing input fields for description, deadline, points of a task, along with a button to update the task
        Ensure that the fields are prepoulated with the values that already exist in the database

        :param:
        :type:
        :raise:
        :return: Blocks list
        :rtype: list

        """

        task = db.session.query(Task).filter_by(task_id=self.current_task_id).all()[0]
        description = str(task.description)
        deadline = str(task.deadline.strftime("%Y-%m-%d"))
        points = str(task.points)

        user_id = db.session.query(Assignment).filter_by(assignment_id=self.current_task_id).all()
        if(user_id): 
            slack_user_id = db.session.query(User).filter_by(user_id=user_id[0].user_id).all()[0].slack_user_id

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

        blocks = []
        blocks.append(block_task_id)
        blocks.append(block_description)
        return blocks



    def update_task(self, id, desc, points, deadline, assignee, created_by):
        print("Update")