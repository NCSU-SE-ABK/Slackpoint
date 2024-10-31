from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.utils import header_property

from commands.viewmytasks import ViewMyTasks
from models import User


class DailyStandupReport:
    """
    This class schedules and sends daily standup reports of tasks via Slack.

    **Why**: Useful for teams who want an automated daily update on tasks, making it easy to track progress,
    manage upcoming deadlines, and keep the team aligned on outstanding tasks directly within Slack.

    **How**: Common usage examples:
    1. `DailyStandupReport.schedule_daily_report(report_time="09:00")`: Set up a daily schedule to automatically send reports.
    2. `DailyStandupReport.send_daily_report()`: Manually trigger sending the daily report.
    3. `DailyStandupReport.get_standup_message(users)`: Generate a message summarizing tasks for each user.
    """

    block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "",
        },
    }

    def __init__(self, app, channel_id):
        """
        Initializes the DailyStandupReport with the app context and Slack channel ID for sending reports.

        :param app: The Flask application context.
        :type app: Flask
        :param channel_id: The ID of the Slack channel where the report will be sent.
        :type channel_id: str

        **Why**: Initialization sets up the app context and the channel where reports will be posted,
        ensuring daily reports are sent to the specified Slack workspace.
        **How**: Example usage -
        ```
        standup_reporter = DailyStandupReport(app, "#standup-channel")
        ```
        """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.app = app
        self.channel_id = channel_id

    def schedule_daily_report(self, report_time="09:00"):
        """
        Schedules the daily standup report to be sent at the specified time each day.

        :param report_time: Time in 'HH:MM' format when the report should be sent.
        :type report_time: str
        :return: None

        **Why**: Automates the daily reporting process by setting a schedule for sending reports, reducing the need for manual reminders.
        **How**: Example usage -
        ```
        standup_reporter.schedule_daily_report(report_time="08:30")
        ```
        """
        hour, minute = map(int, report_time.split(":"))
        now = datetime.now()
        first_run_time = datetime(
            year=now.year, month=now.month, day=now.day, hour=hour, minute=minute
        )

        if first_run_time < now:
            first_run_time += timedelta(days=1)

        self.scheduler.add_job(
            self.send_daily_report,
            "interval",
            days=1,
            next_run_time=first_run_time,
            args=[]
        )

        from app import slack_client
        with self.app.app_context():
            slack_client.chat_postMessage(
                channel=self.channel_id,
                text=f"Daily Standup Report schedule started - scheduled for {report_time}"
            )

    def get_standup_message(self, users):
        """
        Compiles a daily standup message with each user's task status.

        :param users: List of users to include in the report.
        :type users: list of User objects
        :return: A formatted string representing the standup report.
        :rtype: str

        **Why**: Provides a consolidated message of each user’s task status, covering recently completed, upcoming, and past-due tasks.
        **How**: Example usage -
        ```
        message = standup_reporter.get_standup_message(users)
        ```
        """
        final_message = ""

        # Compile a report for each user
        for user in users:
            final_message += f"*Daily Standup Report for <@{user.slack_user_id}>*" + "\n\n"
            final_message += "*Recently completed tasks:*" + "\n"

            recently_completed = ViewMyTasks(user.slack_user_id).get_completed_tasks()
            tasks_added = False
            for block in recently_completed.get("blocks", []):
                text = block.get("text", {}).get("text")
                if text:
                    final_message += text + "\n"
                    tasks_added = True
            if not tasks_added:
                final_message += "None\n"

            final_message += "\n"

            due_soon = ViewMyTasks(user.slack_user_id).get_upcoming_tasks()
            final_message += "*Tasks due soon:*" + "\n"

            tasks_added = False
            for block in due_soon.get("blocks", []):
                text = block.get("text", {}).get("text")
                if text:
                    final_message += text + "\n"
                    tasks_added = True
            if not tasks_added:
                final_message += "None\n"

            final_message += "\n"

            past_due = ViewMyTasks(user.slack_user_id).get_past_due_tasks()
            final_message += "*Tasks past due:*" + "\n"

            tasks_added = False
            for block in past_due.get("blocks", []):
                text = block.get("text", {}).get("text")
                if text:
                    final_message += text + "\n"
                    tasks_added = True
            if not tasks_added:
                final_message += "None\n"

            final_message += "\n\n\n"

        return final_message

    def send_daily_report(self):
        """
        Compiles and sends the daily standup report to the designated Slack channel.

        **Why**: This method directly executes the report generation and sending process, ideal for manual or scheduled execution.
        **How**: Example usage -
        ```
        standup_reporter.send_daily_report()
        ```
        """
        with self.app.app_context():
            users = User.query.all()
            final_message = self.get_standup_message(users)
            self.post_to_slack({"text": {"text": final_message}})

    def post_to_slack(self, report_payload):
        """
        Sends the standup report to a specified Slack channel.

        :param report_payload: The payload of the report in Slack-compatible format.
        :type report_payload: dict
        :return: None

        **Why**: Allows the report to be delivered directly within a Slack channel, ensuring visibility and accessibility for the team.
        **How**: Example usage -
        ```
        report_payload = {"text": {"text": "Sample report"}}
        standup_reporter.post_to_slack(report_payload)
        ```
        """
        try:
            from app import slack_client
            with self.app.app_context():
                blocks = report_payload.get("blocks", [])
                if blocks:
                    slack_client.chat_postMessage(
                        channel=self.channel_id,
                        blocks=blocks
                    )
                else:
                    slack_client.chat_postMessage(
                        channel=self.channel_id,
                        text=report_payload["text"]["text"]
                    )
        except Exception as e:
            print(f"Error sending message to Slack: {e}")
