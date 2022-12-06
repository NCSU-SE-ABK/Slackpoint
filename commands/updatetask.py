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


    def update_task(self, id, desc, points, deadline, assignee, created_by):
        print("Update")