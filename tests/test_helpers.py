# tests/test_errorhelper.py

import pytest
from helpers.errorhelper import ErrorHelper
from dotenv import load_dotenv

load_dotenv()
def test_get_error_payload_blocks(mocker):
    """Test the get_error_payload_blocks function."""
    mock_help = mocker.patch('helpers.errorhelper.Help.help', return_value=[{"type": "section", "text": {"type": "mrkdwn", "text": "Help text"}}])
    error_helper = ErrorHelper()
    blocks = error_helper.get_error_payload_blocks("create")
    assert len(blocks) == 2
    assert blocks[0]["text"]["text"] == ">Oops! Something went wrong. Please try again with the correct command rules."
    assert blocks[1]["text"]["text"] == "Help text"

def test_get_command_help_create():
    """Test the get_command_help function for 'create' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("create")
    assert message.startswith(">To create a task, follow the format:")

def test_get_command_help_no_task_id():
    """Test the get_command_help function for 'no_task_id' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("no_task_id")
    assert message == "The given Task ID does not exist! Please try again..."

def test_get_command_help_task_already_done():
    """Test the get_command_help function for 'task_already_done' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("task_already_done")
    assert message == "The given Task was already completed!"

def test_get_command_help_task_done():
    """Test the get_command_help function for 'task_done' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("task_done")
    assert message == "Congratulations, your task is completed now!"

def test_get_command_help_task_updated():
    """Test the get_command_help function for 'task_updated' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("task_updated")
    assert message == "The task has been updated!"

def test_get_command_help_task_cannot_be_updated():
    """Test the get_command_help function for 'task_cannot_be_updated' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("task_cannot_be_updated")
    assert message == "The task has not been assigned to you."

def test_get_command_help_task_assigned():
    """Test the get_command_help function for 'task_assigned' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("task_assigned", ["User1", 123])
    assert message == "You have been assigned task #123 by User1"

def test_get_command_help_not_created_by_you():
    """Test the get_command_help function for 'not_created_by_you' command."""
    error_helper = ErrorHelper()
    message = error_helper.get_command_help("not_created_by_you")
    assert message == "You cannot modify this task."