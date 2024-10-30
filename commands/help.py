from copy import deepcopy


class Help:
    """
    This class provides help functionality by offering detailed descriptions for each command.

    **Why**: Ideal for users unfamiliar with commands, allowing them to quickly access help details on
    all available commands in the application, streamlining the learning curve and improving usability.

    **How**: Common usage examples:
    1. `Help.help_all()`: Generate help payload with descriptions of all commands.
    2. `Help.help(command_name)`: Generate a help description payload for a specific command.
    """

    commands_dictionary = {}

    command_help = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "{command_help}"},
    }

    def __init__(self):
        """
        Initializes the Help object with a dictionary of commands and their descriptions.

        **Why**: Constructs a dictionary of available commands with examples and descriptions,
        making it easy to generate help content on demand.
        **How**: Example usage -
        ```
        help_obj = Help()
        ```
        """
        self.commands_dictionary["createtask"] = [
            "*Create Task*",
            ">To create a task, just try the command */create-task* and you would receive a message from Slack to fill out the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my new task\n>*Deadline*: 12/31/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the generated *Task ID*.",
        ]
        self.commands_dictionary["viewcompleted"] = [
            "*View Completed Tasks*",
            ">To view completed tasks, just try the command */view-completed*, and there you go! SlackPoint would show you a list of completed tasks.",
        ]
        self.commands_dictionary["viewpending"] = [
            "*View Pending Task*",
            ">To view pending tasks, just try the command */view-pending*, and there you go! SlackPoint would show you a list of completed tasks. To view pending tasks only for yourself, just try the command */view-pending me*, and there you go! SlackPoint would show you a list of tasks assigned to you. To view pending tasks due today, just try the command */view-pending today*, and SlackPoint will show you a list of tasks with today's deadline.",
        ]
        self.commands_dictionary["updatetask"] = [
            "*Update Task*",
            ">To update a task, just run the command */update-task* <Task ID>, edit the details and hit submit!",
        ]
        self.commands_dictionary["leaderboard"] = [
            "*Leaderboard*",
            ">To view the leaderboard, just try the command */leaderboard*, and SlackPoint would show you the top five contenders!",
        ]
        self.commands_dictionary["taskdone"] = [
            "*Complete Task*",
            ">To mark a task as Completed, just try the command */task-done* <Task ID>, and now you are one step closer at being one of the top five contenders!",
        ]
        self.commands_dictionary["help"] = [
            "*Help*",
            ">Well, you are viewing it. You don't need my help in that case :D",
        ]

        self.payload = {"response_type": "ephemeral", "blocks": []}

    def help_all(self):
        """
        Generates a payload with help details for all commands.

        :return: A payload object containing helper details for all commands.
        :rtype: dict[str, Any]

        **Why**: Provides an easily accessible, full list of command descriptions for users needing an overview
        or guidance on available functionalities.
        **How**: Example usage -
        ```
        all_help = help_obj.help_all()
        ```
        """
        response_payload = deepcopy(self.payload)
        for name in self.commands_dictionary.keys():
            blocks = self.help(name)
            response_payload["blocks"].extend(blocks)
        return response_payload

    def help(self, command_name):
        """
        Generates a help description payload for a specific command.

        :param command_name: Name of the command to retrieve help for.
        :type command_name: str
        :return: A list of blocks containing details of the specified command.
        :rtype: list

        **Why**: Allows users to access help for a specific command without needing the full list, making it easier
        to find targeted information.
        **How**: Example usage -
        ```
        specific_help = help_obj.help("createtask")
        ```
        """
        blocks = []
        command_name_block = deepcopy(self.command_help)
        command_help_desc_block = deepcopy(self.command_help)
        command_help = self.commands_dictionary.get(command_name)
        command_name_block["text"]["text"] = command_name_block["text"]["text"].format(
            command_help=command_help[0]
        )
        command_help_desc_block["text"]["text"] = command_help_desc_block["text"][
            "text"
        ].format(command_help=command_help[1])

        blocks.append(command_name_block)
        blocks.append(command_help_desc_block)
        return blocks
