from datetime import datetime
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """
    This class represents the Task entity in the database, storing details about tasks such as description,
    points, deadline, and timestamps for creation and updates.

    **Why**: Useful for tracking individual tasks, allowing applications to store, retrieve, and manage task
    details effectively.

    **How**: Common usage examples:
    1. `Task.query.all()`: Retrieve all tasks.
    2. `Task.query.filter_by(task_id=1).first()`: Retrieve a specific task by ID.
    """

    __tablename__ = "task"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    Unique identifier for each task.
    """

    description = db.Column(db.Text())
    """
    Text description of the task.
    """

    points = db.Column(db.Integer)
    """
    Points assigned to the task for tracking effort or priority.
    """

    deadline = db.Column(db.Date)
    """
    Deadline date for task completion.
    """

    created_on = db.Column(db.DateTime, default=datetime.now())
    """
    Timestamp for when the task was created.
    """

    updated_on = db.Column(db.DateTime, default=datetime.now())
    """
    Timestamp for when the task was last updated.
    """

    created_by = db.Column(db.Integer)
    """
    ID of the user who created the task, linking to the User entity.
    """

    __table_args__ = (db.UniqueConstraint("task_id"),)


class Assignment(db.Model):
    """
    This class represents the Assignment entity in the database, storing task assignments and tracking
    progress for each task assigned to users.

    **Why**: Facilitates assignment management by linking tasks to users and tracking their progress,
    enabling task delegation and monitoring.

    **How**: Common usage examples:
    1. `Assignment.query.filter_by(user_id=1).all()`: Retrieve all assignments for a user.
    2. `Assignment.query.filter_by(assignment_id=1).first()`: Retrieve a specific assignment by task ID.
    """

    __tablename__ = "assignment"

    user_id = db.Column(db.Integer, ForeignKey("user.user_id"))
    """
    Foreign key linking to the User table, representing the user assigned to the task.
    """

    assignment_id = db.Column(db.Integer, ForeignKey("task.task_id"), primary_key=True)
    """
    Primary key linking to the Task table, representing the assigned task.
    """

    progress = db.Column(db.Float)
    """
    Progress of the assignment, where `1.0` represents completion.
    """

    assignment_created_on = db.Column(db.DateTime, default=datetime.now())
    """
    Timestamp for when the assignment was created.
    """

    assignment_updated_on = db.Column(db.DateTime)
    """
    Timestamp for when the assignment was last updated.
    """


class User(db.Model):
    """
    This class represents the User entity in the database, storing user information such as unique Slack
    user IDs.

    **Why**: Essential for linking tasks and assignments to specific users, enabling personalized tracking
    and Slack integration.

    **How**: Common usage examples:
    1. `User.query.filter_by(slack_user_id="U12345").first()`: Retrieve a user by Slack ID.
    2. `User.query.all()`: Retrieve all users.
    """

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    Unique identifier for each user.
    """

    slack_user_id = db.Column(db.String, unique=True)
    """
    Unique Slack ID for the user, enabling Slack-specific interactions.
    """

    __table_args__ = (db.UniqueConstraint("user_id"),)
