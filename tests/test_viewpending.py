from unittest.mock import MagicMock
from commands.viewpoints import ViewPoints
from tests.mockmodels import (
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
)


def test_view_pending_2tasks(
    mock_pending_task_1,
    mock_pending_task_2,
    mock_get_sqlalchemy,
):
    """
    Test the view pending command for 2 tasks.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
        mock_pending_task_2,
    ]

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Expectation
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

    assert payload == expected_payload


def test_view_pending_0tasks(
    mock_get_sqlalchemy,
):
    """
    Test the view pending command for 0 tasks.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = []

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Expectation
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

    assert payload == expected_payload


def test_view_pending_1task(mock_pending_task_1, mock_get_sqlalchemy):
    """
    Test the view pending command for 1 task.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
    ]

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Expectation
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

    assert payload == expected_payload


def test_view_pending_sqlalchemy_exception(mock_get_sqlalchemy):
    """
    Test the view pending command with an exception from SQLAlchemy.
    """
    # Mock SQLAlchemy to raise an exception
    mock_get_sqlalchemy.join.side_effect = Exception("Database error")

    # Test function
    vp = ViewPoints(progress=0.0)

    try:
        vp.get_list()
    except Exception as e:
        assert str(e) == "Database error"


def test_view_pending_with_progress(mock_pending_task_1, mock_get_sqlalchemy):
    """
    Test the view pending command with a custom progress value.
    """
    # Mocking DB call
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_pending_task_1,
    ]

    # Test function
    vp = ViewPoints(progress=50.0)
    payload = vp.get_list()

    # Expectation
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

    assert payload == expected_payload



def test_view_pending_large_tasks(mock_get_sqlalchemy):
    """
    Test the view pending command with a large number of tasks.
    """
    # Mocking DB call
    large_tasks = [
        MagicMock(
            task_id=f"SP-{i}",
            points=i,
            description=f"Task {i}",
            deadline="2022-10-24",
        )
        for i in range(1, 101)
    ]

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = large_tasks

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Validate the number of blocks returned
    assert len(payload["blocks"]) == 100



