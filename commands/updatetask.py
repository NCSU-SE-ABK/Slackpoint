from copy import deepcopy
import random
from models import *
from helpers.errorhelper import ErrorHelper
import datetime

class UpdateTask:
    """ 
    This class handles task updates, allowing users to modify existing tasks and reassign task details.

    **Why**: Essential for task management, enabling users to update task properties, including description,
    deadline, points, and assigned users, to ensure accurate and current task tracking.

    **How**: Common usage examples:
    1. `UpdateTask.checkTaskID()`: Verify if the specified task ID exists in the database.
    2. `UpdateTask.create_task_input_blocks()`: Generate Slack-compatible blocks for user input fields prefilled
       with current task data for updating.
    3. `UpdateTask.update_task(id, desc, points, deadline, assignee)`: Update task properties in the database.
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
        Initializes the UpdateTask object with user and task data, setting up the response payload.

        :param user_id: Slack User ID of the user requesting the update.
        :type user_id: str
        :param data: Dictionary containing task-related data, such as task ID.
        :type data: dict
        :param users: List of users available for assignment.
        :type users: list of dicts

        **Why**: Preparation of user and task data allows easy access to details required for validation and
        task updating actions.
        **How**: Example usage -
        ```
        task_update = UpdateTask("U12345", {"text": "12"}, [{"name": "John Doe", "user_id": "U67890"}])
        ```
        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }
        self.user_id = db.session.query(User).filter_by(slack_user_id=user_id).all()[0].user_id
        self.data = data
        self.users = users

    def checkTaskID(self):
        """
        Validates if a given task ID exists in the database.

        :return: Boolean indicating whether the task ID exists.
        :rtype: bool

        **Why**: Ensures that users can only attempt to update tasks that actually exist.
        **How**: Example usage -
        ```
        is_valid = task_update.checkTaskID()
        ```
        """
        helper = ErrorHelper()
        self.current_task_id = int(self.data.get('text'))

        # Check if task ID exists
        exists = db.session.query(db.exists().where(Task.task_id == self.current_task_id)).scalar()
        if exists:
            return True
        else:
            helper.get_command_help("no_task_id")

    def create_task_input_blocks(self):
        """
        Creates Slack-compatible input blocks prefilled with current task details for easy updating.

        :return: List of blocks for task input fields, including description, deadline, points, and assignees.
        :rtype: list

        **Why**: Provides users with prefilled input fields, making it easy to update tasks without manually
        re-entering existing data.
        **How**: Example usage -
        ```
        input_blocks = task_update.create_task_input_blocks()
        ```
        """
        task = db.session.query(Task).filter_by(task_id=self.current_task_id).all()[0]
        description = str(task.description)
        deadline = str(task.deadline.strftime("%Y-%m-%d"))
        points = str(task.points)

        user_id = db.session.query(Assignment).filter_by(assignment_id=self.current_task_id).all()
        if user_id:
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
                    {
                        "text": {"type": "plain_text", "text": "1", "emoji": False},
                        "value": "1",
                    },
                    {
                        "text": {"type": "plain_text", "text": "2", "emoji": False},
                        "value": "2",
                    },
                    {
                        "text": {"type": "plain_text", "text": "3", "emoji": False},
                        "value": "3",
                    },
                    {
                        "text": {"type": "plain_text", "text": "4", "emoji": False},
                        "value": "4",
                    },
                    {
                        "text": {"type": "plain_text", "text": "5", "emoji": False},
                        "value": "5",
                    },
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
            placeholder = {"text": {"type": "plain_text", "emoji": False}}
            placeholder["text"]["text"] = user["name"]
            placeholder["value"] = user["user_id"]
            if user["user_id"] == slack_user_id:
                selectedUser = placeholder
            block_users["element"]["options"].append(placeholder)

        block_users["element"]["initial_option"] = selectedUser

        block_actions_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Update task"
            },
            "action_id": "update_action_button",
            "value": str(self.current_task_id)
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = [
            block_task_id,
            block_description,
            block_deadline,
            block_points,
            block_users,
            block_actions
        ]
        return blocks

    def update_task(self, id, desc, points, deadline, assignee):
        """
        Updates task properties in the database and returns a success message payload.

        :param id: Task ID to be updated.
        :type id: int
        :param desc: Updated description of the task.
        :type desc: str
        :param points: Updated points for the task.
        :type points: int
        :param deadline: Updated deadline for the task.
        :type deadline: str
        :param assignee: Slack ID of the user assigned to the task.
        :type assignee: str
        :return: Payload blocks with success message if update is successful.
        :rtype: list

        **Why**: Updates ensure task data is current and assigned to the appropriate user, facilitating effective
        task tracking.
        **How**: Example usage -
        ```
        response_payload = task_update.update_task(12, "New Description", 3, "2023-12-31", "U67890")
        ```
        """
        response = deepcopy(self.base_create_task_block_format)

        creatorUserId = Task.query.filter_by(task_id=id).all()[0].created_by
        sameUser = (creatorUserId == self.user_id)
        if not sameUser:
            response["text"]["text"] = "You are not allowed to make changes to this task."
        else:
            # Ensure assignee exists in User table
            exists = db.session.query(db.exists().where(User.slack_user_id == assignee)).scalar()
            if not exists:
                user = User()
                user.slack_user_id = assignee
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)

                # Get user ID from User table
            user_id = User.query.filter_by(slack_user_id=assignee).all()[0].user_id

            # Update task in Task table
            db.session.query(Task).filter_by(task_id=id).update(dict(description=desc, points=points, deadline=deadline))
            db.session.commit()

            # Update assignment in Assignment table
            db.session.query(Assignment).filter_by(assignment_id=id).update(dict(user_id=user_id))
            db.session.commit()

            response["text"]["text"] = response["text"]["text"].format(greeting=random.choice(self.greetings), id=id)

        self.payload["blocks"].append(response)
        return self.payload["blocks"]
