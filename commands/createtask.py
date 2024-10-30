from copy import deepcopy
import random
from models import *


class CreateTask:
    """
    This class handles task creation functionality, including user assignment and
    Slack-compatible response generation to confirm task creation.

    **Why**: Motivation for use cases where automated task creation and assignment are needed,
    especially in environments leveraging Slack for task management, making it easier to
    create, assign, and confirm tasks within a collaborative workspace.

    **How**: Common usage examples:
    1. `CreateTask.create_task_input_blocks()`: Prepares the Slack-compatible input UI for task details.
    2. `CreateTask.create_task(desc, points, deadline, assignee, created_by)`: Creates a task with
       specified attributes and stores it in the database.
    """

    base_create_task_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">{greeting}! Your task SP-{id} was created successfully.",
        },
    }

    greetings = ["Awesome", "Great", "Congratulations", "Well done", "Let's go"]

    def __init__(self, users=[]):
        """
        Initializes the CreateTask object with optional users for assignment.

        :param users: List of users available for task assignment.
        :type users: list of dict, each with 'name' and 'user_id' keys.
        :return: None

        **Why**: Use this constructor to initialize the payload and user list for assignment options.
        **How**: Example usage -
        ```
        users = [{"name": "John Doe", "user_id": "U12345"}]
        task_creator = CreateTask(users)
        ```
        """
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }
        self.users = users

    def create_task_input_blocks(self):
        """
        Creates a list of Slack-compatible input blocks for task creation.

        :return: A list of blocks, each representing an input field or button.
        :rtype: list

        **Why**: This function provides Slack's interactive message structure, allowing users to input
        task details like description, deadline, points, and assignees in a standardized format.
        **How**: Example usage -
        ```
        blocks = task_creator.create_task_input_blocks()
        ```
        """
        block_description = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "create_action_description",
            },
            "label": {"type": "plain_text", "text": "Description", "emoji": True},
        }
        block_deadline = {
            "type": "input",
            "element": {
                "type": "datepicker",
                "initial_date": "2022-01-01",
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

        for user in self.users:
            placeholder =  {"text": {"type": "plain_text", "emoji": False}}
            placeholder["text"]["text"] = user["name"]
            placeholder["value"] = user["user_id"]
            block_users["element"]["options"].append(placeholder)

        block_actions_button = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Create task"
            },
            "action_id": "create_action_button",
        }
        block_actions = {"type": "actions", "elements": []}
        block_actions["elements"].append(block_actions_button)

        blocks = []
        blocks.append(block_description)
        blocks.append(block_deadline)
        blocks.append(block_points)
        blocks.append(block_users)
        blocks.append(block_actions)
        return blocks

    def create_task(self, desc, points, deadline, assignee, created_by):
        """
        Creates a task in the database and prepares a success message with task ID.

        :param desc: Description of task
        :type desc: str
        :param points: Points of task
        :type points: int
        :param deadline: Deadline of task
        :type deadline: Date
        :param assignee: User ID of the assignee
        :type assignee: str
        :param created_by: User ID of the creator
        :type created_by: str
        :return: Response blocks and Task ID
        :rtype: tuple(list, int)

        **Why**: Provides an efficient way to manage task records in the database, while generating a
        Slack-friendly confirmation message for the task creator.
        **How**: Example usage -
        ```
        response, task_id = task_creator.create_task("New feature", 3, "2023-12-01", "U67890", "U12345")
        ```
        """
        # DB call to add task, returns id
        task = Task()
        task.description = desc
        task.points = points
        task.deadline = deadline

        exists = db.session.query(db.exists().where(User.slack_user_id == created_by)).scalar()
        if not exists:
            user = User()
            user.slack_user_id = created_by
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        created_user_id = User.query.filter_by(slack_user_id=created_by).all()[0].user_id

        task.created_by = created_user_id
        db.session.add(task)
        db.session.commit()
        db.session.refresh(task)

        # task id
        id = task.task_id

        exists = db.session.query(db.exists().where(User.slack_user_id == assignee)).scalar()
        if not exists:
            user = User()
            user.slack_user_id = assignee
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)


        # add the task in assignment, depending on whether assignee is None or not
        assignment = Assignment()
        assignment.assignment_id = id
        if assignee is not None:
            assignee_user_id = User.query.filter_by(slack_user_id=assignee).all()
            assignment.user_id = assignee_user_id[0].user_id
        assignment.progress = 0
        db.session.add(assignment)
        db.session.commit()

        response = deepcopy(self.base_create_task_block_format)
        response["text"]["text"] = response["text"]["text"].format(greeting=random.choice(self.greetings), id=id)
        self.payload["blocks"].append(response)
        return self.payload["blocks"], id
