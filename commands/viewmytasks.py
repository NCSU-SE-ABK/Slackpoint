from copy import deepcopy
from datetime import timedelta
from models import *

class ViewMyTasks:
    """
    This class retrieves and displays tasks assigned to a specific user, categorized by completion,
    due dates, and pending status.

    **Why**: Ideal for users wanting a personalized view of their tasks, making it easy to track task progress,
    stay on top of deadlines, and manage workload effectively within Slack.

    **How**: Common usage examples:
    1. `ViewMyTasks.get_completed_tasks(delta=48)`: Retrieve tasks completed in the past 48 hours.
    2. `ViewMyTasks.get_upcoming_tasks(delta=7)`: Retrieve tasks due in the next 7 days.
    3. `ViewMyTasks.get_past_due_tasks()`: Retrieve overdue tasks.
    4. `ViewMyTasks.get_list()`: Retrieve all current tasks with pending progress.
    """

    base_point_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">SP-{id} ({points} SlackPoints) {description} [Deadline: {deadline}]",
        },
    }

    def __init__(self, user_id):
        """
        Initializes the ViewMyTasks class for a specific user by Slack ID and sets up the response payload.

        :param user_id: Slack User ID of the user for whom tasks are being retrieved.
        :type user_id: str

        **Why**: Prepares the class with user-specific data, enabling personalized task retrieval.
        **How**: Example usage -
        ```
        my_tasks = ViewMyTasks("U12345")
        ```
        """
        self.user_id = user_id
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def get_completed_tasks(self, delta=48):
        """
        Fetches tasks completed within a specified time frame (default: 48 hours).

        :param delta: Time frame in hours for fetching recently completed tasks.
        :type delta: int
        :return: Slack message payload containing recently completed tasks.
        :rtype: dict

        **Why**: Allows users to track tasks completed recently, assisting in progress reporting.
        **How**: Example usage -
        ```
        completed_tasks = my_tasks.get_completed_tasks(delta=24)
        ```
        """
        user_id = User.query.filter_by(slack_user_id=self.user_id).all()[0].user_id
        last_24_hours = datetime.now() - timedelta(hours=delta)
        completed_tasks = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.user_id,
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Assignment.user_id == user_id)
            .filter(Assignment.progress == 1)  # Completed tasks
            .filter(Task.updated_on >= last_24_hours)  # Completed in the last specified hours
            .all()
        )

        for task in completed_tasks:
            point = deepcopy(self.base_point_block_format)
            point["text"]["text"] = point["text"]["text"].format(
                id=task.task_id,
                points=task.points,
                description=task.description,
                deadline=task.deadline,
            )
            self.payload["blocks"].append(point)

        return self.payload

    def get_upcoming_tasks(self, delta=7):
        """
        Fetches tasks due within the next specified number of days (default: 7 days).

        :param delta: Time frame in days for fetching upcoming tasks.
        :type delta: int
        :return: Slack message payload containing upcoming tasks.
        :rtype: dict

        **Why**: Helps users prioritize tasks due soon, providing visibility on deadlines approaching.
        **How**: Example usage -
        ```
        upcoming_tasks = my_tasks.get_upcoming_tasks(delta=5)
        ```
        """
        user_id = User.query.filter_by(slack_user_id=self.user_id).all()[0].user_id
        next_week = datetime.now() + timedelta(days=delta)
        upcoming_tasks = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.user_id,
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Assignment.user_id == user_id)
            .filter(Assignment.progress < 1)  # Incomplete tasks
            .filter(Task.deadline <= next_week)
            .filter(Task.deadline >= datetime.now()) # Tasks due within a week
            .all()
        )

        for task in upcoming_tasks:
            point = deepcopy(self.base_point_block_format)
            point["text"]["text"] = point["text"]["text"].format(
                id=task.task_id,
                points=task.points,
                description=task.description,
                deadline=task.deadline,
            )
            self.payload["blocks"].append(point)

        return self.payload

    def get_past_due_tasks(self):
        """
        Fetches tasks that are overdue and have not been completed.

        :return: Slack message payload containing past-due tasks.
        :rtype: dict

        **Why**: Alerts users to overdue tasks, helping them catch up and manage pending tasks.
        **How**: Example usage -
        ```
        past_due_tasks = my_tasks.get_past_due_tasks()
        ```
        """
        user_id = User.query.filter_by(slack_user_id=self.user_id).all()[0].user_id
        old_tasks = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.user_id,
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Assignment.user_id == user_id)
            .filter(Assignment.progress < 1)  # Incomplete tasks
            .filter(Task.deadline < datetime.now().date()) # Tasks due before now
            .all()
        )

        for task in old_tasks:
            point = deepcopy(self.base_point_block_format)
            point["text"]["text"] = point["text"]["text"].format(
                id=task.task_id,
                points=task.points,
                description=task.description,
                deadline=task.deadline,
            )
            self.payload["blocks"].append(point)

        return self.payload

    def get_list(self):
        """
        Retrieves a list of all tasks that are incomplete, formatted for Slack display.

        :return: Slack message payload containing all pending tasks for the user.
        :rtype: dict

        **Why**: Provides an overview of all outstanding tasks, assisting in task management and prioritization.
        **How**: Example usage -
        ```
        task_list = my_tasks.get_list()
        ```
        """
        tasks = []
        user_id = User.query.filter_by(slack_user_id=self.user_id).all()[0].user_id
        tasks_with_progress = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.user_id,
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Assignment.user_id == user_id)
            .filter(Assignment.progress < 1)
            .all()
        )
        tasks.extend(tasks_with_progress)

        # Format tasks for Slack display
        for task in tasks:
            point = deepcopy(self.base_point_block_format)
            point["text"]["text"] = point["text"]["text"].format(
                id=task.task_id,
                points=task.points,
                description=task.description,
                deadline=task.deadline,
            )
            self.payload["blocks"].append(point)
        if not self.payload["blocks"]:
            self.payload["blocks"].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ">Currently there are no SlackPoints available",
                    },
                }
            )
        return self.payload
