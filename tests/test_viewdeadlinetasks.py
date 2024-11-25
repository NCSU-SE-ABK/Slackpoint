from commands.viewdeadlinetasks import ViewDeadlineTasks
from commands.viewpoints import ViewPoints
from tests.mockmodels import (
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
)
from unittest.mock import MagicMock


# Test Cases for ViewDeadlineTasks
def test_view_deadline_tasks(
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
):
    """
    Test the view deadline tasks command with two tasks.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
        mock_pending_task_2,
    ]

    # Test function
    vp = ViewDeadlineTasks()
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-1 (10 SlackPoints) This is Task 1 [Deadline: 2022-10-24]",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-2 (2 SlackPoints) This is Task 2 [Deadline: 2022-10-26]",
                },
            },
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"


def test_view_deadline_tasks_single_task(
    mock_pending_task_1,
    mock_get_sqlalchemy,
):
    """
    Test the view deadline tasks command with one task.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
    ]

    # Test function
    vp = ViewDeadlineTasks()
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-1 (10 SlackPoints) This is Task 1 [Deadline: 2022-10-24]",
                },
            }
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"


# Test Cases for ViewPoints
def test_view_pending_0tasks(mock_get_sqlalchemy):
    """
    Test the view pending command for 0 tasks.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = []

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">Currently there are no SlackPoints available",
                },
            }
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"


def test_view_pending_tasks_zero_progress(mock_pending_task_2, mock_get_sqlalchemy):
    """
    Test the view pending tasks with tasks having zero progress.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_2,
    ]

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-2 (2 SlackPoints) This is Task 2 [Deadline: 2022-10-26]",
                },
            }
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"


def test_view_pending_tasks_with_progress_lessthan50_2(mock_pending_task_1, mock_get_sqlalchemy):
    """cls
    Test the view pending tasks with non-zero progress.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
    ]

    # Test function
    vp = ViewPoints(progress=40.0)
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-1 (10 SlackPoints) This is Task 1 [Deadline: 2022-10-24]",
                },
            }
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"

def test_view_pending_tasks_with_progress_lessthan50(mock_pending_task_1, mock_get_sqlalchemy):
    """
    Test the view pending tasks with non-zero progress.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
    ]

    # Test function
    vp = ViewPoints(progress=30.0)
    payload = vp.get_list()

    # Expected output
    expected_payload = {
        "response_type": "ephemeral",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ">SP-1 (10 SlackPoints) This is Task 1 [Deadline: 2022-10-24]",
                },
            }
        ],
    }

    assert payload == expected_payload, f"Payload mismatch:\nExpected: {expected_payload}\nActual: {payload}"


