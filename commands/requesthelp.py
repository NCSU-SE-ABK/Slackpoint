from copy import deepcopy
from models import Task, Assignment, User, db
from helpers.errorhelper import ErrorHelper

class RequestHelp:
    """
    This class handles the "Request Help" functionality, allowing users to request assistance from teammates
    for a specific task.

    **Why**: Provides a streamlined way for users to notify teammates when they need assistance on a task,
    helping foster collaboration and efficient task management.

    **How**: Common usage examples:
    1. `RequestHelp.request_help()`: Validate task status and send help requests to specified teammates.
    2. `RequestHelp.validate_task_and_user(task_id, user_id)`: Check if a task is assigned to the user and
       still incomplete.
    """

    base_request_help_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">You requested help for Task SP-{id}. Teammates have been notified.",
        },
    }

    def __init__(self, app, data, teammates=[]):
        """
        Initializes the RequestHelp instance with the Flask app context, request data, and list of teammates.

        :param app: Flask app instance for context.
        :type app: Flask
        :param data: Data for the help request, including task ID and user details.
        :type data: dict
        :param teammates: List of teammates to notify, with Slack user IDs and names.
        :type teammates: list[dict]

        **Why**: Sets up the request details and teammate list, enabling easy access to data for processing
        the help request.
        **How**: Example usage -
        ```
        request_help = RequestHelp(app, data={"text": "12 @teammate1"}, teammates=teammate_list)
        ```
        """
        self.app = app
        self.data = data
        self.teammates = teammates
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def validate_task_and_user(self, task_id, user_id):
        """
        Validates if the specified task exists, is assigned to the user, and is incomplete.

        :param task_id: Task ID to validate.
        :type task_id: int
        :param user_id: Slack user ID of the requester.
        :type user_id: str
        :return: Tuple indicating if the task is valid and an error message if not.
        :rtype: tuple(bool, str)

        **Why**: Ensures the help request is valid by checking if the task exists, is assigned to the requesting
        user, and is still open.
        **How**: Example usage -
        ```
        is_valid, error_message = request_help.validate_task_and_user(12, "U12345")
        ```
        """
        with self.app.app_context():
            helper = ErrorHelper()

            # Check if task exists
            task = Task.query.filter_by(task_id=task_id).first()
            if not task:
                return False, helper.get_command_help("no_task_id")

            # Check if the user is assigned to the task and it's incomplete
            assignment = Assignment.query.filter_by(assignment_id=task_id).first()
            if not assignment or assignment.progress == 1.0:
                return False, helper.get_command_help("task_already_done")

            return True, ""

    def process_help_command(self, command_parts):
        task_id = int(command_parts[0])  # Task ID should be the first part of the command
        user_id = self.data.get("user_id")

        # Validate task existence, ownership, and completion status
        valid, message = self.validate_task_and_user(task_id, user_id)
        if not valid:
            return message

        # Extract teammate IDs
        teammate_slack_ids = [
            part for part in command_parts[1:] if part.startswith("@")
        ]

        teammate_slack_ids = [x[1:] for x in teammate_slack_ids]

        # check teammates array where username is the slack_id and user_id is what we want instead
        teammate_slack_user_ids = []
        for x in teammate_slack_ids:
            for teammate in self.teammates:
                if x == teammate["username"]:
                    teammate_slack_user_ids.append(teammate["user_id"])

        return task_id, user_id, teammate_slack_user_ids

    def request_help(self):
        """
        Processes the help request by validating the task and notifying teammates.

        :return: Payload with success message or error message.
        :rtype: dict
        """
        from app import slack_client
        with self.app.app_context():
            # Parse task ID and teammate IDs from the command
            command_parts = self.data.get('text').split()

            if len(command_parts) < 2 or not command_parts[0].isdigit():
                response = deepcopy(self.base_request_help_block_format)
                response["text"]["text"] = "Format: /requesthelp {id} {@teammate1} [@teammate2] ..."
                self.payload["blocks"].append(response)
                return self.payload

            task_id, user_id, teammate_slack_user_ids = self.process_help_command(command_parts)

            # Notify teammates
            task_info = f"Task SP-{task_id}. Assigned to <@{user_id}>."
            notification_text = f"<@{user_id}> is requesting help with:\n{task_info}"

            for slack_id in teammate_slack_user_ids:
                dm_response = slack_client.conversations_open(users=slack_id)

                if dm_response["ok"]:
                    dm_channel = dm_response["channel"]["id"]
                    slack_client.chat_postMessage(
                        channel=dm_channel,
                        text=notification_text
                    )
                else:
                    slack_client.chat_postMessage(
                        channel=f"Failed to open DM with {slack_id}: {dm_response['error']}",
                        text=notification_text
                    )

            # Confirmation message to requester
            response = deepcopy(self.base_request_help_block_format)
            response["text"]["text"] = response["text"]["text"].format(id=task_id)
            self.payload["blocks"].append(response)

            if not self.payload["blocks"]:
                self.payload["text"] = "Help request sent, but no teammates were specified."

            return self.payload