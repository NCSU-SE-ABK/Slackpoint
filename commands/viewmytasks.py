from copy import deepcopy
from datetime import timedelta

from models import *
class ViewMyTasks:
    """
    This class is used to view a list of tasks on the slack bot as per the user they have been assigned to
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
        Initialise ViewTasks Class. Set progress for filtering tasks.

        :param progress: Optional Filter on tasks according to their progress.
        :type progress: float
        :raise:
        :return: ViewPoints object
        :rtype: ViewPoints object

        """
        self.user_id = user_id
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def get_completed_tasks(self, delta=48):
        """
        Fetch tasks completed since the last daily report (within the last x (default:24) hours).
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
            .filter(Task.updated_on >= last_24_hours)  # Completed in the last 24 hours
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
        Fetch tasks due in the next x (default:7) days that are not completed.
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
        Fetch tasks due already that are not completed.
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
        Return a list of tasks formatted in a slack message payload.

        :param None:
        :type None:
        :raise None:
        :return: Slack message payload with list of tasks.
        :rtype: dict

        """
        tasks = []
        # db query to get all tasks that have progress < 1

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

        # parse them
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