from models import Task, Assignment
from tests.mockmodels import mock_my_model, mock_get_sqlalchemy


def test_sqlalchemy_query_property_get_mock(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test the view pending command

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQL Alchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool

    """
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Assignment.progress == 1.0)
        .all()
    )

    assert response == [mock_my_model]
    
def test_sqlalchemy_query_for_completed_tasks(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test query to fetch tasks where the progress is marked as 1 (completed)

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQLAlchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool
    """
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Assignment.progress == 1.0)  # Completed tasks
        .all()
    )

    assert response == [mock_my_model]

def test_sqlalchemy_query_for_incomplete_tasks(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test query to fetch tasks where the progress is less than 1 (incomplete)

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQLAlchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool
    """
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Assignment.progress < 1.0)  # Incomplete tasks
        .all()
    )

    assert response == [mock_my_model]

from datetime import datetime

def test_sqlalchemy_query_for_tasks_by_deadline(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test query to fetch tasks with a specific deadline

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQLAlchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool
    """
    specific_date = datetime(2024, 12, 31)

    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Task.deadline == specific_date)
        .all()
    )

    assert response == [mock_my_model]

def test_sqlalchemy_query_for_tasks_with_high_points(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test query to fetch tasks with points greater than a specific value

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQLAlchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool
    """
    mock_my_model.points = 100  # Mocked points value
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Task.points > 50)  # Filter tasks with points greater than 50
        .all()
    )

    assert response == [mock_my_model]

def test_sqlalchemy_query_for_tasks_by_keyword(
    mock_my_model,
    mock_get_sqlalchemy,
):
    """
    Test query to fetch tasks with descriptions containing a specific keyword

    :param mock_my_model: Mocked Task object
    :type mock_my_model: Task
    :param mock_get_sqlalchemy: Mocked SQLAlchemy object
    :type mock_get_sqlalchemy: Any
    :raise:
    :return: Assert if test case executed successfully
    :rtype: bool
    """
    keyword = "important"  # Keyword to filter the description

    mock_my_model.description = "This is an important task"  # Mocked description
    mock_get_sqlalchemy.join.return_value.add_columns.return_value.filter.return_value.all.return_value = [
        mock_my_model
    ]
    response = (
        Task.query.join(Assignment)
        .add_columns(
            Assignment.progress,
            Task.task_id,
            Task.points,
            Task.description,
            Task.deadline,
        )
        .filter(Task.description.ilike(f"%{keyword}%"))  # Search for tasks containing the keyword
        .all()
    )

    assert response == [mock_my_model]

