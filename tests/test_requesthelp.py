import pytest
from commands.requesthelp import RequestHelp

def test_process_help_command_multiple_valid_teammates(mocker):
    """
    Test process_help_command with a valid task ID and multiple valid teammate usernames.
    """
    # Setup
    command_parts = ["1", "@teammate1", "@teammate2"]
    user_id = "U123456"
    teammates = [
        {"username": "teammate1", "user_id": "T123456"},
        {"username": "teammate2", "user_id": "T654321"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (1, user_id, ["T123456", "T654321"])
    validate_mock.assert_called_once_with(1, user_id)


def test_process_help_command_single_valid_teammate(mocker):
    """
    Test process_help_command with a valid task ID and a single valid teammate username.
    """
    # Setup
    command_parts = ["2", "@teammate1"]
    user_id = "U654321"
    teammates = [
        {"username": "teammate1", "user_id": "T654321"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (2, user_id, ["T654321"])
    validate_mock.assert_called_once_with(2, user_id)

def test_process_help_command_no_teammates(mocker):
    """
    Test process_help_command with a valid task ID but no teammates specified.
    """
    # Setup
    command_parts = ["3"]
    user_id = "U111111"
    teammates = []
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (3, user_id, [])
    validate_mock.assert_called_once_with(3, user_id)

def test_process_help_command_missing_task_id(mocker):
    """
    Test process_help_command with missing task ID in the command.
    """
    # Setup
    command_parts = []
    user_id = "U222222"
    teammates = [
        {"username": "teammate1", "user_id": "T222222"},
    ]
    data = {"user_id": user_id}

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute and Assert
    with pytest.raises(IndexError):
        request_help.process_help_command(command_parts)


def test_process_help_command_non_digit_task_id(mocker):
    """
    Test process_help_command with a non-digit task ID.
    """
    # Setup
    command_parts = ["ABC", "@teammate1"]
    user_id = "U333333"
    teammates = [
        {"username": "teammate1", "user_id": "T333333"},
    ]
    data = {"user_id": user_id}

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute and Assert
    with pytest.raises(ValueError):
        request_help.process_help_command(command_parts)


def test_process_help_command_task_does_not_exist(mocker):
    """
    Test process_help_command where the task ID does not exist.
    """
    # Setup
    command_parts = ["4", "@teammate1"]
    user_id = "U444444"
    teammates = [
        {"username": "teammate1", "user_id": "T444444"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (False, "Task does not exist.")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(False, "Task does not exist."))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == "Task does not exist."
    validate_mock.assert_called_once_with(4, user_id)

def test_process_help_command_task_already_complete(mocker):
    """
    Test process_help_command where the task is already complete.
    """
    # Setup
    command_parts = ["5", "@teammate1"]
    user_id = "U555555"
    teammates = [
        {"username": "teammate1", "user_id": "T555555"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (False, "Task is already complete.")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(False, "Task is already complete."))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == "Task is already complete."
    validate_mock.assert_called_once_with(5, user_id)

def test_process_help_command_user_not_assigned(mocker):
    """
    Test process_help_command where the user is not assigned to the specified task.
    """
    # Setup
    command_parts = ["6", "@teammate1"]
    user_id = "U666666"
    teammates = [
        {"username": "teammate1", "user_id": "T666666"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (False, "User not assigned to this task.")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(False, "User not assigned to this task."))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == "User not assigned to this task."
    validate_mock.assert_called_once_with(6, user_id)


def test_process_help_command_teammate_username_not_found(mocker):
    """
    Test process_help_command where the specified teammate username is not found in the teammates list.
    """
    # Setup
    command_parts = ["7", "@unknown1"]
    user_id = "U777777"
    teammates = [
        {"username": "teammate1", "user_id": "T777777"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (7, user_id, [])
    validate_mock.assert_called_once_with(7, user_id)



def test_process_help_command_teammate_similar_but_distinct(mocker):
    """
    Test process_help_command where teammate usernames are similar but distinct.
    """
    # Setup
    command_parts = ["8", "@teammate1", "@teammate2"]
    user_id = "U888888"
    teammates = [
        {"username": "teammate1", "user_id": "T888888"},
        {"username": "teammate2", "user_id": "T999999"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (8, user_id, ["T888888", "T999999"])
    validate_mock.assert_called_once_with(8, user_id)


def test_process_help_command_duplicate_teammate_usernames(mocker):
    """
    Test process_help_command with duplicate teammate usernames in the command.
    """
    # Setup
    command_parts = ["9", "@teammate1", "@teammate1"]
    user_id = "U999999"
    teammates = [
        {"username": "teammate1", "user_id": "T999999"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (9, user_id, ["T999999", "T999999"])
    validate_mock.assert_called_once_with(9, user_id)



def test_process_help_command_teammate_usernames_missing_at(mocker):
    """
    Test process_help_command where teammate usernames do not start with '@'.
    """
    # Setup
    command_parts = ["10", "teammate1", "teammate2"]
    user_id = "U101010"
    teammates = [
        {"username": "teammate1", "user_id": "T101010"},
        {"username": "teammate2", "user_id": "T202020"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (10, user_id, [])
    validate_mock.assert_called_once_with(10, user_id)


def test_process_help_command_extra_whitespace(mocker):
    """
    Test process_help_command with extra whitespace in the command.
    """
    # Setup
    command_parts = ["11", "@teammate1", "   ", "@teammate2", " "]
    user_id = "U111111"
    teammates = [
        {"username": "teammate1", "user_id": "T111111"},
        {"username": "teammate2", "user_id": "T222222"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    # The command_parts include empty strings which do not start with '@'
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (11, user_id, ["T111111", "T222222"])
    validate_mock.assert_called_once_with(11, user_id)



def test_process_help_command_mixed_valid_invalid_teammates(mocker):
    """
    Test process_help_command with a mix of valid and invalid teammate usernames.
    """
    # Setup
    command_parts = ["12", "@teammate1", "@invalid1", "@teammate2", "@invalid2"]
    user_id = "U121212"
    teammates = [
        {"username": "teammate1", "user_id": "T121212"},
        {"username": "teammate2", "user_id": "T222222"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (12, user_id, ["T121212", "T222222"])
    validate_mock.assert_called_once_with(12, user_id)




def test_process_help_command_teammate_usernames_different_cases(mocker):
    """
    Test process_help_command where teammate usernames have different cases.
    """
    # Setup
    command_parts = ["13", "@TeAmAtE1", "@teammate2"]
    user_id = "U131313"
    teammates = [
        {"username": "teammate1", "user_id": "T131313"},
        {"username": "teammate2", "user_id": "T232323"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    # Assuming username matching is case-sensitive
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (13, user_id, ["T232323"])  # Only "teammate2" matches
    validate_mock.assert_called_once_with(13, user_id)


def test_process_help_command_teammate_usernames_empty_strings(mocker):
    """
    Test process_help_command with teammate usernames as empty strings.
    """
    # Setup
    command_parts = ["14", "@", "@teammate1", "@"]
    user_id = "U141414"
    teammates = [
        {"username": "teammate1", "user_id": "T141414"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (14, user_id, ["T141414"])  # Only "@teammate1" is valid
    validate_mock.assert_called_once_with(14, user_id)


def test_process_help_command_teammate_usernames_special_characters(mocker):
    """
    Test process_help_command with teammate usernames containing special characters.
    """
    # Setup
    command_parts = ["15", "@teammate_1", "@teammate#2"]
    user_id = "U151515"
    teammates = [
        {"username": "teammate_1", "user_id": "T151515"},
        {"username": "teammate#2", "user_id": "T252525"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (15, user_id, ["T151515", "T252525"])
    validate_mock.assert_called_once_with(15, user_id)


def test_process_help_command_teammate_usernames_none(mocker):
    """
    Test process_help_command with teammate usernames as None.
    """
    # Setup
    command_parts = ["16", "@teammate1", "@None"]
    user_id = "U161616"
    teammates = [
        {"username": "teammate1", "user_id": "T161616"},
        {"username": "None", "user_id": "T262626"},
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    assert result == (16, user_id, ["T161616", "T262626"])
    validate_mock.assert_called_once_with(16, user_id)


def test_process_help_command_large_number_of_teammates(mocker):
    """
    Test process_help_command with a large number of teammate usernames.
    """
    # Setup
    task_id = 17
    user_id = "U171717"
    teammates = [{"username": f"teammate{i}", "user_id": f"T{i}"} for i in range(1, 21)]  # 20 teammates
    teammate_usernames = [f"@teammate{i}" for i in range(1, 21)]
    command_parts = [str(task_id)] + teammate_usernames
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    expected_user_ids = [f"T{i}" for i in range(1, 21)]
    assert result == (17, user_id, expected_user_ids)
    validate_mock.assert_called_once_with(17, user_id)



def test_process_help_command_teammate_usernames_with_at_symbols(mocker):
    """
    Test process_help_command where teammate usernames contain additional '@' symbols.
    """
    # Setup
    command_parts = ["18", "@@teammate1", "@teammate2@"]
    user_id = "U181818"
    teammates = [
        {"username": "@teammate1", "user_id": "T181818"},  # Username starts with '@'
        {"username": "teammate2@", "user_id": "T282828"},  # Username ends with '@'
    ]
    data = {"user_id": user_id}

    # Mock validate_task_and_user to return (True, "")
    validate_mock = mocker.patch.object(RequestHelp, 'validate_task_and_user', return_value=(True, ""))

    # Instantiate RequestHelp
    request_help = RequestHelp(app=None, data=data, teammates=teammates)

    # Execute
    result = request_help.process_help_command(command_parts)

    # Assert
    # Extracted usernames will be "@teammate1" and "teammate2@"
    assert result == (18, user_id, ["T181818", "T282828"])
    validate_mock.assert_called_once_with(18, user_id)

