import pytest
from unittest.mock import MagicMock, patch
from commands.taskdone import TaskDone
from helpers.errorhelper import ErrorHelper
from models import Assignment, Task, User


@pytest.fixture
def mock_error_helper():
    error_helper = MagicMock()
    error_helper.get_command_help.side_effect = lambda key: {
        "no_task_id": "Task ID does not exist!",
        "task_already_done": "The given Task was already completed!",
        "task_done": "Task marked as completed successfully!",
        "task_cannot_be_updated": "You are not allowed to update this task!"
    }[key]
    return error_helper



@patch('commands.taskdone.db.session')
def test_task_already_done(mock_db_session, mock_error_helper):
    """
    Test case for when the task is already completed.
    """
    mock_db_session.query.return_value.scalar.return_value = True  # Task exists
    mock_db_session.query.return_value.filter_by.return_value.all.return_value = []  # Task progress is not 0.0

    data = {"text": "123", "user_id": "U12345"}
    td = TaskDone(data)
    td.helper = mock_error_helper

    assert td.update_points() == "The given Task was already completed!"

@patch('commands.taskdone.db.session')
def test_task_already_done1(mock_db_session, mock_error_helper):
    """
    Test case for when the task is already completed.
    """
    mock_db_session.query.return_value.scalar.return_value = True  # Task exists
    mock_db_session.query.return_value.filter_by.return_value.all.return_value = []  # Task progress is not 0.0

    data = {"text": "587", "user_id": "X45895"}
    td = TaskDone(data)
    td.helper = mock_error_helper

    assert td.update_points() == "The given Task was already completed!"

@patch('commands.taskdone.db.session')
def test_task_already_done2(mock_db_session, mock_error_helper):
    """
    Test case for when the task is already completed.
    """
    mock_db_session.query.return_value.scalar.return_value = True  # Task exists
    mock_db_session.query.return_value.filter_by.return_value.all.return_value = []  # Task progress is not 0.0

    data = {"text": "256", "user_id": "U4702"}
    td = TaskDone(data)
    td.helper = mock_error_helper

    assert td.update_points() == "The given Task was already completed!"



@patch('commands.taskdone.db.session')
def test_no_task_id(mock_db_session):
    mock_db_session.query.return_value.scalar.return_value = False  # Task ID does not exist
    data = {"text": "999", "user_id": "U12345"}
    td = TaskDone(data)
    assert td.update_points() == "The given Task ID does not exist! Please try again..."

@patch('commands.taskdone.db.session')
def test_no_task_id1(mock_db_session):
    mock_db_session.query.return_value.scalar.return_value = False  # Task ID does not exist
    data = {"text": "529", "user_id": "A0987"}
    td = TaskDone(data)
    assert td.update_points() == "The given Task ID does not exist! Please try again..."

@patch('commands.taskdone.db.session')
def test_no_task_id2(mock_db_session):
    mock_db_session.query.return_value.scalar.return_value = False  # Task ID does not exist
    data = {"text": "3032", "user_id": "J8037"}
    td = TaskDone(data)
    assert td.update_points() == "The given Task ID does not exist! Please try again..."