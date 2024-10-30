from models import *
from helpers.errorhelper import ErrorHelper


class TaskDone:
    """
    This class manages task completion, including validation and updating task status.

    **Why**: Useful for ensuring tasks are marked as completed by authorized users, maintaining task
    progression integrity in a collaborative environment, and handling user-specific task updates.

    **How**: Common usage examples:
    1. `TaskDone.get_or_create(uid)`: Retrieve or create a user based on Slack ID.
    2. `TaskDone.update_points()`: Complete a task and update points if the user has authorization.
    """

    def __init__(self, data):
        """
        Initializes TaskDone with the task data and response payload template.

        :param data: Dictionary containing task data, including user and task IDs.
        :type data: dict

        **Why**: Initial setup for the class allows task data and payload to be prepared, making it easy to
        handle task updates and user interactions.
        **How**: Example usage -
        ```
        task_data = {"user_id": "U12345", "text": "12"}
        task_done = TaskDone(task_data)
        ```
        """
        self.data = data
        self.payload = {
            "response_type": "ephemeral",
            "blocks": []
        }

    def get_or_create(self, uid):
        """
        Fetches a user instance by Slack ID or creates a new one if it doesn’t exist.

        :param uid: Slack User ID to retrieve or create.
        :type uid: str
        :return: User instance fetched or created from the database.
        :rtype: User

        **Why**: Ensures that a user exists in the database, allowing for task assignments and updates
        to be correctly associated with a Slack user.
        **How**: Example usage -
        ```
        user = task_done.get_or_create("U12345")
        ```
        """
        instance = db.session.query(User).filter_by(slack_user_id=uid).first()
        if instance:
            return instance
        else:
            instance = db.session.add(User(slack_user_id=uid))
            db.session.commit()
            return instance

    def update_points(self):
        """
        Marks a task as complete, validating that the task exists and that the requesting user is authorized.

        :return: Success message if task completion is successful; error message if validation fails.
        :rtype: str

        **Why**: Provides controlled task completion, only allowing assigned users to mark tasks as completed.
        **How**: Example usage -
        ```
        result = task_done.update_points()
        ```
        """
        helper = ErrorHelper()
        current_task_id = int(self.data.get('text'))
        current_slack_id = self.data.get('user_id')

        # Check if task exists
        exists = db.session.query(db.exists().where(Task.task_id == current_task_id)).scalar()

        task_progress = Assignment.query.filter_by(assignment_id=current_task_id, progress=0.0).all()

        if not exists:
            return helper.get_command_help("no_task_id")

        # Check if task is already done
        elif exists and len(task_progress) == 0:
            return helper.get_command_help("task_already_done")

        # Process task if not yet done
        elif exists and task_progress[0].progress == 0.0:

            my_query = self.get_or_create(current_slack_id)

            # Validate that the user marking the task as complete is the assigned user
            userId = db.session.query(Assignment).filter_by(assignment_id=current_task_id).all()[0].user_id
            sameUser = db.session.query(User).filter_by(slack_user_id=current_slack_id).all()[0].user_id == userId

            if sameUser:
                user_id = my_query.user_id

                task_assignment = db.session.query(Assignment).filter_by(assignment_id=current_task_id).first()
                task_assignment.progress = 1.0
                task_assignment.user_id = user_id
                task_assignment.updated_on = datetime.now()
                db.session.commit()
                return helper.get_command_help("task_done")
            else:
                return helper.get_command_help("task_cannot_be_updated")
