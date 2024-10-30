import os

# Set environment variables before importing app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SLACK_SIGNING_SECRET'] = "ACTIONS_SLACK_SIGNING_SECRET"
os.environ['SLACK_BOT_TOKEN'] = "ACTIONS_SLACK_BOT_TOKEN"
os.environ['VERIFICATION_TOKEN'] = "ACTIONS_VERIFICATION_TOKEN"

import pytest
from flask import Flask
from app import db
from commands.dailystandupreport import DailyStandupReport  # Adjust as needed
from models import User, Task, Assignment  # Adjust as needed

@pytest.fixture
def app_instance():
    """
    Create and configure a new app instance for each test session.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False  # Disable SQL echo for tests
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    """
    A test client for the app.
    """
    return app_instance.test_client()

@pytest.fixture
def mock_slack_client(mocker):
    """
    Mock the Slack client from the app module.
    """
    return mocker.patch('app.slack_client')

@pytest.fixture
def mock_scheduler(mocker):
    """
    Mock the BackgroundScheduler used in DailyStandupReport.
    """
    scheduler = mocker.patch('commands.dailystandupreport.BackgroundScheduler')
    return scheduler

@pytest.fixture
def daily_report(app_instance, mock_scheduler):
    """
    Provide an instance of DailyStandupReport for testing.
    """
    return DailyStandupReport(app_instance, "C07T6TACHJA")  # Replace with your test channel ID

@pytest.fixture
def mock_user(mocker):
    """
    Create a mock User instance.
    """
    user = mocker.Mock(spec=User)
    user.slack_user_id = "U123456"
    return user

@pytest.fixture
def mock_users(mocker, mock_user):
    """
    Return a list of mock users.
    """
    return [mock_user]

@pytest.fixture
def mock_completed_tasks(mocker):
    """
    Create a list of mock completed Task instances.
    """
    completed_task = mocker.Mock(spec=Task)
    completed_task.task_id = 1
    completed_task.points = 10
    completed_task.description = "Completed Task 1"
    completed_task.deadline = "2024-10-20"
    return [completed_task]

@pytest.fixture
def mock_upcoming_tasks(mocker):
    """
    Create a list of mock upcoming Task instances.
    """
    upcoming_task = mocker.Mock(spec=Task)
    upcoming_task.task_id = 2
    upcoming_task.points = 5
    upcoming_task.description = "Upcoming Task 1"
    upcoming_task.deadline = "2024-11-01"
    return [upcoming_task]

@pytest.fixture
def mock_past_due_tasks(mocker):
    """
    Create a list of mock past due Task instances.
    """
    past_due_task = mocker.Mock(spec=Task)
    past_due_task.task_id = 3
    past_due_task.points = 8
    past_due_task.description = "Past Due Task 1"
    past_due_task.deadline = "2024-09-30"
    return [past_due_task]