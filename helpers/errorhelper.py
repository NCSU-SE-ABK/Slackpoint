from copy import deepcopy
from commands.help import Help


class ErrorHelper:
    """
    This class provides standardized error handling and command help messaging for Slack bot interactions.

    **Why**: Simplifies error reporting by formatting consistent and informative error messages, which include
    helpful command usage information to guide users.

    **How**: Common usage examples:
    1. `ErrorHelper.get_error_payload_blocks(command)`: Retrieve error blocks with help information for a specific command.
    2. `ErrorHelper.get_command_help(command)`: Retrieve a customized error message for a specific command.
    """

    error_payload = {"response_type": "ephemeral", "blocks": []}
    error_block_1 = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">Oops! Something went wrong. Please try again with the correct command rules.",
        },
    }

    def __init__(self) -> None:
        """
        Initializes the ErrorHelper with a Help instance for providing command-specific help messages.

        **Why**: Sets up access to command help documentation, allowing dynamic error handling with usage guidance.
        **How**: Example usage -
        ```
        error_helper = ErrorHelper()
        ```
        """
        self.command_help = Help()

    def get_error_payload_blocks(self, command):
        """
        Retrieves error message blocks with help information for a specified command.

        :param command: Command name to provide help for.
        :type command: str
        :return: List of formatted error blocks for Slack display.
        :rtype: list[dict[str, Any]]

        **Why**: Combines a generic error message with command-specific help, giving users clarity on how
        to correct their input.
        **How**: Example usage -
        ```
        error_blocks = error_helper.get_error_payload_blocks("create")
        ```
        """
        error = deepcopy(self.error_payload)
        errorBlock_1 = deepcopy(self.error_block_1)
        errorBlock_2 = self.command_help.help(command_name=command)
        error["blocks"].append(errorBlock_1)
        error["blocks"].extend(errorBlock_2)
        return error["blocks"]

    def get_command_help(self, command, args=[]):
        """
        Retrieves an error message with usage instructions or details for a specific command.

        :param command: Command name for which help or an error message is needed.
        :type command: str
        :param args: Optional arguments for customizing certain messages.
        :type args: list
        :return: Formatted error or help message for the specified command.
        :rtype: str

        **Why**: Provides specific feedback and guidance for users on errors or command usage.
        **How**: Example usage -
        ```
        help_message = error_helper.get_command_help("task_done")
        ```
        """
        command_help = ""
        if command == "create":
            command_help = ">To create a task, follow the format: \n*-d* [description of task] *-p* [points of the task] *-ddl* [deadline of the task].\nFor example: */create* *-d* Hey! This is my new task *-p* 100 *-ddl* 15/10/2022"
        elif command == "no_task_id":
            command_help = "The given Task ID does not exist! Please try again..."
        elif command == "task_already_done":
            command_help = "The given Task was already completed!"
        elif command == "task_done":
            command_help = "Congratulations, your task is completed now!"
        elif command == "task_updated":
            command_help = "The task has been updated!"
        elif command == "task_cannot_be_updated":
            command_help = "The task has not been assigned to you."
        elif command == "task_assigned":
            command_help = f"You have been assigned task #{args[1]} by {args[0]}"
        elif command == "not_created_by_you":
            command_help = "You cannot modify this task."
        return command_help
