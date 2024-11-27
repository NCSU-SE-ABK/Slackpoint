import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.help import Help # type: ignore


def test_help():
    """
    Test the help command
    """
    h = Help()
    payload = h.help_all()

    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Create Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To create a task, just try the command */create-task* and you would receive a message from Slack to fill out the details of the task.\n>Enter the description, deadline and the points of the task.\n>For example:\n>*Description*: Hey! This is my new task\n>*Deadline*: 12/31/2022 (just select a date from the date picker)\n>*Points*: 5 (select a point from 1 to 5)\n>And that's it! You should receive a reply from Slack with the generated *Task ID*.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*View Completed Tasks*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view completed tasks, just try the command */view-completed*, and there you go! SlackPoint would show you a list of completed tasks.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*View Pending Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view pending tasks, just try the command */view-pending*, and there you go! SlackPoint would show you a list of completed tasks. To view pending tasks only for yourself, just try the command */view-pending me*, and there you go! SlackPoint would show you a list of tasks assigned to you. To view pending tasks due today, just try the command */view-pending today*, and SlackPoint will show you a list of tasks with today's deadline.",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Update Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To update a task, just run the command */update-task* <Task ID>, edit the details and hit submit!",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Leaderboard*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To view the leaderboard, just try the command */leaderboard*, and SlackPoint would show you the top five contenders!",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Complete Task*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">To mark a task as Completed, just try the command */task-done* <Task ID>, and now you are one step closer at being one of the top five contenders!",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Help*"}},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">Well, you are viewing it. You don't need my help in that case :D",
                },
            },
        ],
    }

    print(payload)
    print("*************")
    print(expected_payload)
    assert payload == expected_payload