from copy import deepcopy
from models import *

class ViewDeadlineTasks:
    """
    This class retrieves and displays tasks due today in a Slack-compatible format.

    **Why**: Useful for users to see tasks with deadlines on the current day, aiding in prioritizing tasks
    and managing time effectively.

    **How**: Common usage examples:
    1. `ViewDeadlineTasks.get_list()`: Retrieve a list of tasks due today in a formatted Slack message payload.
    """

    base_point_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">SP-{id} ({points} SlackPoints) {description} [Deadline: {deadline}]",
        },
    }

    def __init__(self):
        """
        Initializes the ViewDeadlineTasks class and sets up the response payload template.

        **Why**: Prepares the payload structure for displaying task lists, ensuring compatibility with
        Slack’s message format.
        **How**: Example usage -
        ```
        deadline_tasks = ViewDeadlineTasks()
        ```
        """
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def get_list(self):
        """
        Retrieves a list of tasks due today, formatted for display in Slack.

        :return: Slack message payload containing tasks due today.
        :rtype: dict

        **Why**: Provides an easy-to-access list of urgent tasks, helping users stay informed about upcoming
        deadlines and ensuring timely task completion.
        **How**: Example usage -
        ```
        tasks_due_today = deadline_tasks.get_list()
        ```
        """
        tasks = []

        # Database query to retrieve tasks due today with progress < 1 (not completed)
        tasks_with_deadline = (
            Task.query.join(Assignment)
            .add_columns(
                Assignment.user_id,
                Assignment.progress,
                Task.task_id,
                Task.points,
                Task.description,
                Task.deadline,
            )
            .filter(Task.deadline == datetime.now().strftime("%Y-%m-%d"))
            .filter(Assignment.progress < 1)
            .all()
        )
        tasks.extend(tasks_with_deadline)

        # Parse tasks and format them for Slack
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
