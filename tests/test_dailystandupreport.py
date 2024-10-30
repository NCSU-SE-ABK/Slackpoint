import pytest
from unittest.mock import MagicMock, patch

from commands.dailystandupreport import DailyStandupReport
from models import User, Task, Assignment

# Fixture to create a list of mock User instances
@pytest.fixture
def mock_users(mocker):
    """
    Fixture to create a list of mock User instances.
    """
    user1 = mocker.Mock(spec=User)
    user1.slack_user_id = "U123456"
    user2 = mocker.Mock(spec=User)
    user2.slack_user_id = "U654321"
    return [user1, user2]

# Fixture to provide an instance of DailyStandupReport for testing
@pytest.fixture
def daily_report(app_instance, mock_scheduler):
    """
    Fixture to provide an instance of DailyStandupReport for testing.
    """
    return DailyStandupReport(app_instance, "C07T6TACHJA")  # Replace with your test channel ID

def test_daily_report_exists(daily_report, mock_users, mocker):
    assert daily_report is not None

def test_get_standup_message_multiple_users_all_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with multiple users, each having all task categories populated.
    """
    # Create mocks for each user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 1.1"}}, {"text": {"text": "Completed Task 1.2"}}]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 1.1"}}, {"text": {"text": "Upcoming Task 1.2"}}]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 1.1"}}, {"text": {"text": "Past Due Task 1.2"}}]
    }

    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 2.1"}}, {"text": {"text": "Completed Task 2.2"}}]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 2.1"}}, {"text": {"text": "Upcoming Task 2.2"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 2.1"}}, {"text": {"text": "Past Due Task 2.2"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Return a default mock if needed

    # Patch the ViewMyTasks to use the side_effect function
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 1.1\n"
        "Completed Task 1.2\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 1.1\n"
        "Upcoming Task 1.2\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 1.1\n"
        "Past Due Task 1.2\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 2.1\n"
        "Completed Task 2.2\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 2.1\n"
        "Upcoming Task 2.2\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 2.1\n"
        "Past Due Task 2.2\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_multiple_users_some_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with multiple users, some task categories populated.
    """
    # Create mocks for each user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 1"}}]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": []  # No upcoming tasks
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 1"}}]
    }

    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": []  # No completed tasks
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 2"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": []  # No past due tasks
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 1\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 1\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 2\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_multiple_users_no_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with multiple users, none having any tasks.
    """
    # Create mocks for each user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {"blocks": []}
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {"blocks": []}
    view_my_tasks_instance1.get_past_due_tasks.return_value = {"blocks": []}

    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {"blocks": []}
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {"blocks": []}
    view_my_tasks_instance2.get_past_due_tasks.return_value = {"blocks": []}

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_single_user_all_tasks(daily_report, mocker):
    """
    Test get_standup_message with a single user, all task categories populated.
    """
    # Create a single mock user
    mock_user = mocker.Mock(spec=User)
    mock_user.slack_user_id = "U123456"
    mock_users = [mock_user]

    # Mock ViewMyTasks methods
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')
    view_my_tasks_instance = MagicMock()
    view_my_tasks_instance.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task A"}}, {"text": {"text": "Completed Task B"}}]
    }
    view_my_tasks_instance.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task A"}}]
    }
    view_my_tasks_instance.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task A"}}]
    }
    view_my_tasks_mock.return_value = view_my_tasks_instance

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task A\n"
        "Completed Task B\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task A\n\n"
        "*Tasks past due:*\n"
        "Past Due Task A\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_single_user_some_tasks(daily_report, mocker):
    """
    Test get_standup_message with a single user, some task categories populated.
    """
    # Create a single mock user
    mock_user = mocker.Mock(spec=User)
    mock_user.slack_user_id = "U123456"
    mock_users = [mock_user]

    # Mock ViewMyTasks methods
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')
    view_my_tasks_instance = MagicMock()
    view_my_tasks_instance.get_completed_tasks.return_value = {"blocks": []}  # No completed tasks
    view_my_tasks_instance.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task A"}}]
    }
    view_my_tasks_instance.get_past_due_tasks.return_value = {"blocks": []}  # No past due tasks
    view_my_tasks_mock.return_value = view_my_tasks_instance

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task A\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_single_user_no_tasks(daily_report, mocker):
    """
    Test get_standup_message with a single user, no tasks in any category.
    """
    # Create a single mock user
    mock_user = mocker.Mock(spec=User)
    mock_user.slack_user_id = "U123456"
    mock_users = [mock_user]

    # Mock ViewMyTasks methods
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')
    view_my_tasks_instance = MagicMock()
    view_my_tasks_instance.get_completed_tasks.return_value = {"blocks": []}
    view_my_tasks_instance.get_upcoming_tasks.return_value = {"blocks": []}
    view_my_tasks_instance.get_past_due_tasks.return_value = {"blocks": []}
    view_my_tasks_mock.return_value = view_my_tasks_instance

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_no_users(daily_report, mocker):
    """
    Test get_standup_message with no users provided.
    """
    mock_users = []

    # Define expected message
    expected_message = ""

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message is empty
    assert final_message == expected_message

def test_get_standup_message_multiple_tasks_each_category(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having multiple tasks in each category.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Completed Task 1.1"}},
            {"text": {"text": "Completed Task 1.2"}},
            {"text": {"text": "Completed Task 1.3"}}
        ]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Upcoming Task 1.1"}},
            {"text": {"text": "Upcoming Task 1.2"}}
        ]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Past Due Task 1.1"}}
        ]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Completed Task 2.1"}}
        ]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": []
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Past Due Task 2.1"}},
            {"text": {"text": "Past Due Task 2.2"}}
        ]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 1.1\n"
        "Completed Task 1.2\n"
        "Completed Task 1.3\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 1.1\n"
        "Upcoming Task 1.2\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 1.1\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 2.1\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 2.1\n"
        "Past Due Task 2.2\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_special_characters_in_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with special characters and markdown in task descriptions.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "*Completed Task 1* with **bold** and _italic_ text."}}]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 1 with [link](http://example.com)"}}]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 1 with `code` snippet."}}]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 2 with emojis 🎉🚀"}}]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 2 with special characters: @#$%^&*()"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 2 with non-ASCII characters: 測試"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "*Completed Task 1* with **bold** and _italic_ text.\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 1 with [link](http://example.com)\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 1 with `code` snippet.\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 2 with emojis 🎉🚀\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 2 with special characters: @#$%^&*()\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 2 with non-ASCII characters: 測試\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_empty_blocks_key(daily_report, mock_users, mocker):
    """
    Test get_standup_message when 'blocks' key is missing in task categories.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user: 'blocks' key missing
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {}
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {}
    view_my_tasks_instance1.get_past_due_tasks.return_value = {}

    # Mock for second user: 'blocks' key missing
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {}
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {}
    view_my_tasks_instance2.get_past_due_tasks.return_value = {}

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_malformed_task_data(daily_report, mock_users, mocker):
    """
    Test get_standup_message with malformed task data (missing 'text' key).
    """
    # Create mocks for each user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"content": "Completed Task 1"}}]  # Incorrect key
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 1"}}]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 1"}}]
    }

    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"content": {"text": "Completed Task 2"}}]  # Incorrect structure
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 2"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 2"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message (assuming missing 'text' results in 'None')
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"  # Malformed data treated as no tasks
        "*Tasks due soon:*\n"
        "Upcoming Task 1\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 1\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"  # Malformed data treated as no tasks
        "*Tasks due soon:*\n"
        "Upcoming Task 2\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 2\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_large_number_of_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having a large number of tasks.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Generate a large number of tasks for first user
    completed_tasks_user1 = [{"text": {"text": f"Completed Task 1.{i}"}} for i in range(1, 101)]
    upcoming_tasks_user1 = [{"text": {"text": f"Upcoming Task 1.{i}"}} for i in range(1, 51)]
    past_due_tasks_user1 = [{"text": {"text": f"Past Due Task 1.{i}"}} for i in range(1, 21)]

    # Generate a large number of tasks for second user
    completed_tasks_user2 = [{"text": {"text": f"Completed Task 2.{i}"}} for i in range(1, 76)]
    upcoming_tasks_user2 = [{"text": {"text": f"Upcoming Task 2.{i}"}} for i in range(1, 31)]
    past_due_tasks_user2 = [{"text": {"text": f"Past Due Task 2.{i}"}} for i in range(1, 11)]

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {"blocks": completed_tasks_user1}
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {"blocks": upcoming_tasks_user1}
    view_my_tasks_instance1.get_past_due_tasks.return_value = {"blocks": past_due_tasks_user1}

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {"blocks": completed_tasks_user2}
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {"blocks": upcoming_tasks_user2}
    view_my_tasks_instance2.get_past_due_tasks.return_value = {"blocks": past_due_tasks_user2}

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Construct expected_message dynamically due to large number of tasks
    completed_tasks_str_user1 = "\n".join([f"Completed Task 1.{i}" for i in range(1, 101)]) + "\n\n"
    upcoming_tasks_str_user1 = "\n".join([f"Upcoming Task 1.{i}" for i in range(1, 51)]) + "\n\n"
    past_due_tasks_str_user1 = "\n".join([f"Past Due Task 1.{i}" for i in range(1, 21)]) + "\n\n\n\n"

    completed_tasks_str_user2 = "\n".join([f"Completed Task 2.{i}" for i in range(1, 76)]) + "\n\n"
    upcoming_tasks_str_user2 = "\n".join([f"Upcoming Task 2.{i}" for i in range(1, 31)]) + "\n\n"
    past_due_tasks_str_user2 = "\n".join([f"Past Due Task 2.{i}" for i in range(1, 11)]) + "\n\n\n\n"

    expected_message = (
        f"*Daily Standup Report for <@U123456>*\n\n"
        f"*Recently completed tasks:*\n"
        f"{completed_tasks_str_user1}"
        f"*Tasks due soon:*\n"
        f"{upcoming_tasks_str_user1}"
        f"*Tasks past due:*\n"
        f"{past_due_tasks_str_user1}"
        f"*Daily Standup Report for <@U654321>*\n\n"
        f"*Recently completed tasks:*\n"
        f"{completed_tasks_str_user2}"
        f"*Tasks due soon:*\n"
        f"{upcoming_tasks_str_user2}"
        f"*Tasks past due:*\n"
        f"{past_due_tasks_str_user2}"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_identical_tasks(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having identical tasks across categories.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    identical_task = {"text": {"text": "Task 1"}}

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [identical_task]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [identical_task]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Task 1\n\n"
        "*Tasks due soon:*\n"
        "Task 1\n\n"
        "*Tasks past due:*\n"
        "Task 1\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Task 1\n\n"
        "*Tasks due soon:*\n"
        "Task 1\n\n"
        "*Tasks past due:*\n"
        "Task 1\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_similar_but_distinct_slack_ids(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having similar but distinct Slack user IDs.
    """
    # Modify mock_users to have similar but distinct IDs
    mock_users[0].slack_user_id = "U123456"
    mock_users[1].slack_user_id = "U123457"

    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task A"}}]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task A"}}]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task A"}}]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task B"}}]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task B"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task B"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U123457':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task A\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task A\n\n"
        "*Tasks past due:*\n"
        "Past Due Task A\n\n\n\n"
        "*Daily Standup Report for <@U123457>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task B\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task B\n\n"
        "*Tasks past due:*\n"
        "Past Due Task B\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_same_tasks_different_users(daily_report, mock_users, mocker):
    """
    Test get_standup_message with different users having the same tasks.
    """
    identical_task = {"text": {"text": "Same Task"}}

    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [identical_task]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [identical_task]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [identical_task]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Same Task\n\n"
        "*Tasks due soon:*\n"
        "Same Task\n\n"
        "*Tasks past due:*\n"
        "Same Task\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Same Task\n\n"
        "*Tasks due soon:*\n"
        "Same Task\n\n"
        "*Tasks past due:*\n"
        "Same Task\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_users_without_slack_id(daily_report, mocker):
    """
    Test get_standup_message with users missing 'slack_user_id'.
    """
    # Create mock users with 'slack_user_id' set to None
    mock_user1 = mocker.Mock(spec=User)
    mock_user1.slack_user_id = None
    mock_user2 = mocker.Mock(spec=User)
    mock_user2.slack_user_id = None
    mock_users = [mock_user1, mock_user2]

    # Create mocks for each user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {"blocks": [{"text": {"text": "Completed Task 1"}}]}
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {"blocks": [{"text": {"text": "Upcoming Task 1"}}]}
    view_my_tasks_instance1.get_past_due_tasks.return_value = {"blocks": [{"text": {"text": "Past Due Task 1"}}]}

    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {"blocks": [{"text": {"text": "Completed Task 2"}}]}
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {"blocks": [{"text": {"text": "Upcoming Task 2"}}]}
    view_my_tasks_instance2.get_past_due_tasks.return_value = {"blocks": [{"text": {"text": "Past Due Task 2"}}]}

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message (assuming 'None' is displayed for missing slack_user_id)
    expected_message = (
        "*Daily Standup Report for <@None>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
        "*Daily Standup Report for <@None>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_users_with_none_slack_id(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having 'slack_user_id' as None.
    """
    # Set slack_user_id to None for both users
    for user in mock_users:
        user.slack_user_id = None

    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {"blocks": [{"text": {"text": "Completed Task 1"}}]}
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {"blocks": [{"text": {"text": "Upcoming Task 1"}}]}
    view_my_tasks_instance1.get_past_due_tasks.return_value = {"blocks": [{"text": {"text": "Past Due Task 1"}}]}

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {"blocks": [{"text": {"text": "Completed Task 2"}}]}
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {"blocks": [{"text": {"text": "Upcoming Task 2"}}]}
    view_my_tasks_instance2.get_past_due_tasks.return_value = {"blocks": [{"text": {"text": "Past Due Task 2"}}]}

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message (assuming 'None' is displayed for missing slack_user_id)
    expected_message = (
        "*Daily Standup Report for <@None>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
        "*Daily Standup Report for <@None>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_unicode_characters(daily_report, mock_users, mocker):
    """
    Test get_standup_message with unicode characters in task descriptions.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 🚀"}}]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 😊"}}]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task 😱"}}]
    }

    # Mock for second user
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"text": {"text": "Completed Task 🎉"}}]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"text": {"text": "Upcoming Task 🛠️"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"text": {"text": "Past Due Task ⚠️"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 🚀\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 😊\n\n"
        "*Tasks past due:*\n"
        "Past Due Task 😱\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 🎉\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 🛠️\n\n"
        "*Tasks past due:*\n"
        "Past Due Task ⚠️\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message

def test_get_standup_message_mixed_valid_and_invalid_task_data(daily_report, mock_users, mocker):
    """
    Test get_standup_message with users having mixed valid and invalid task data.
    """
    # Mock ViewMyTasks methods for each user
    view_my_tasks_mock = mocker.patch('commands.dailystandupreport.ViewMyTasks')

    # Mock for first user: valid and invalid tasks
    view_my_tasks_instance1 = MagicMock()
    view_my_tasks_instance1.get_completed_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Completed Task 1"}},
            {"invalid_key": {"text": "Invalid Task"}},  # Invalid block
            {"text": {"text": "Completed Task 2"}}
        ]
    }
    view_my_tasks_instance1.get_upcoming_tasks.return_value = {
        "blocks": [
            {"text": {"text": "Upcoming Task 1"}},
            {"text": {"text": "Upcoming Task 2"}}
        ]
    }
    view_my_tasks_instance1.get_past_due_tasks.return_value = {
        "blocks": []  # No past due tasks
    }

    # Mock for second user: all invalid tasks
    view_my_tasks_instance2 = MagicMock()
    view_my_tasks_instance2.get_completed_tasks.return_value = {
        "blocks": [{"invalid_key": {"text": "Invalid Task"}}]
    }
    view_my_tasks_instance2.get_upcoming_tasks.return_value = {
        "blocks": [{"invalid_key": {"text": "Invalid Task"}}]
    }
    view_my_tasks_instance2.get_past_due_tasks.return_value = {
        "blocks": [{"invalid_key": {"text": "Invalid Task"}}]
    }

    # Define a side_effect function to return the correct mock based on user_slack_id
    def view_my_tasks_side_effect(user_slack_id):
        if user_slack_id == 'U123456':
            return view_my_tasks_instance1
        elif user_slack_id == 'U654321':
            return view_my_tasks_instance2
        else:
            return MagicMock()  # Default mock

    # Patch the ViewMyTasks to use the side_effect function
    mocker.patch('commands.dailystandupreport.ViewMyTasks', side_effect=view_my_tasks_side_effect)

    # Define expected message (invalid tasks treated as 'None' or skipped)
    expected_message = (
        "*Daily Standup Report for <@U123456>*\n\n"
        "*Recently completed tasks:*\n"
        "Completed Task 1\n"
        "Completed Task 2\n\n"
        "*Tasks due soon:*\n"
        "Upcoming Task 1\n"
        "Upcoming Task 2\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
        "*Daily Standup Report for <@U654321>*\n\n"
        "*Recently completed tasks:*\n"
        "None\n\n"
        "*Tasks due soon:*\n"
        "None\n\n"
        "*Tasks past due:*\n"
        "None\n\n\n\n"
    )

    # Call get_standup_message
    final_message = daily_report.get_standup_message(mock_users)

    # Assert the final_message matches the expected_message
    assert final_message == expected_message