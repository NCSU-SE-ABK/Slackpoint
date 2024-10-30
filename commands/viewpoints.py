from copy import deepcopy
from models import Task, Assignment

class ViewPoints:
    """
    This class retrieves and displays tasks filtered by their completion progress, formatted for Slack.

    **Why**: Useful for users who want to view tasks based on their completion status, providing a clear view of
    tasks in progress or those that are completed.

    **How**: Common usage examples:
    1. `ViewPoints(progress=0.0).get_list()`: Retrieve a list of tasks that are incomplete.
    2. `ViewPoints(progress=1.0).get_list()`: Retrieve a list of tasks that are completed.
    """

    base_point_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">SP-{id} ({points} SlackPoints) {description} [Deadline: {deadline}]",
        },
    }

    def __init__(self, progress: float = 0.0):
        """
        Initializes the ViewPoints class with a specified progress filter for tasks.

        :param progress: Filter to retrieve tasks based on their completion progress.
        :type progress: float

        **Why**: Allows users to filter tasks by their status, e.g., viewing only completed or incomplete tasks.
        **How**: Example usage -
        ```
        view_points = ViewPoints(progress=0.0)
        ```
        """
        self.progress = progress
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def get_list(self):
        """
        Retrieves tasks with the specified progress status, formatted for Slack.

        :return: Slack message payload containing tasks with the specified progress status.
        :rtype: dict

        **Why**: Provides users with a filtered list of tasks, either completed or in progress, helping them
        stay organized and track their workload effectively.
        **How**: Example usage -
        ```
        task_list = view_points.get_list()
        ```
        """
        tasks = []
        # Database query to get tasks with the specified progress status
        tasks_with_progress = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Assignment.progress == self.progress)
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

        # Handle case when no tasks match the filter
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
