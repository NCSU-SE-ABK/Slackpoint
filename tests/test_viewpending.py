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

def test_view_pending_task_with_zero_points(mock_get_sqlalchemy):
    """
    Test the view pending command with a task having 0 SlackPoints.
    """
    # Mocking DB call
    task_with_zero_points = MagicMock()
    task_with_zero_points.task_id = "2"
    task_with_zero_points.points = 0
    task_with_zero_points.description = "This is Task 2"
    task_with_zero_points.deadline = "2022-10-25"

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        task_with_zero_points,
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
                    "text": ">SP-2 (0 SlackPoints) This is Task 2 [Deadline: 2022-10-25]",
                },
            }
        ],
    }

    assert payload == expected_payload

def test_view_pending_large_tasks_with_new_details(mock_get_sqlalchemy):
    """
    Test the view pending command with a large number of tasks with new details.
    """
    # Mocking DB call
    large_tasks = [
        MagicMock(
            task_id=f"SP-{i}",
            points=i * 2,
            description=f"Task Description {i}",
            deadline="2023-11-01",
        )
        for i in range(1, 101)
    ]

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = large_tasks

    # Test function
    vp = ViewPoints(progress=0.0)
    payload = vp.get_list()

    # Validate the number of blocks returned
    assert len(payload["blocks"]) == 100

def test_view_pending_task_with_new_zero_points(mock_get_sqlalchemy):
    """
    Test the view pending command with a task having 0 SlackPoints and new details.
    """
    # Mocking DB call
    task_with_zero_points = MagicMock()
    task_with_zero_points.task_id = "10"
    task_with_zero_points.points = 0
    task_with_zero_points.description = "Complete initial setup"
    task_with_zero_points.deadline = "2024-01-15"

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        task_with_zero_points,
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
                    "text": ">SP-10 (0 SlackPoints) Complete initial setup [Deadline: 2024-01-15]",
                },
            }
        ],
    }

    assert payload == expected_payload


def test_view_pending_task_with_non_zero_points(mock_get_sqlalchemy):
    """
    Test the view pending command with a task having non-zero SlackPoints.
    """
    # Mocking DB call
    task_with_points = MagicMock()
    task_with_points.task_id = "3"
    task_with_points.points = 10
    task_with_points.description = "This is Task 3"
    task_with_points.deadline = "2024-12-15"

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        task_with_points,
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
                    "text": ">SP-3 (10 SlackPoints) This is Task 3 [Deadline: 2024-12-15]",
                },
            }
        ],
    }

    assert payload == expected_payload

def test_view_pending_task_with_high_points_and_past_deadline(mock_get_sqlalchemy):
    """
    Test the view pending command with a task having high SlackPoints and a past deadline.
    """
    # Mocking DB call
    task_with_high_points = MagicMock()
    task_with_high_points.task_id = "5"
    task_with_high_points.points = 50
    task_with_high_points.description = "Complete Project Alpha"
    task_with_high_points.deadline = "2023-05-10"

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        task_with_high_points,
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
                    "text": ">SP-5 (50 SlackPoints) Complete Project Alpha [Deadline: 2023-05-10]",
                },
            }
        ],
    }

    assert payload == expected_payload
