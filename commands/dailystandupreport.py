from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.utils import header_property

from commands.viewmytasks import ViewMyTasks
from models import User


class DailyStandupReport:
    """
    This class schedules and sends daily standup reports of tasks via Slack.
    """

    block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "",
        },
    }

    def __init__(self, channel_id):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.channel_id = channel_id

    def schedule_daily_report(self, report_time="09:00"):
        """
        Schedules the daily report at the specified time.

        :param report_time: Time in 'HH:MM' format when the report should be sent.
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

        # Use app context to send a message when scheduling is complete
        with self.app.app_context():
            from app import slack_client
            slack_client.chat_postMessage(
                channel=self.channel_id,
                text=f"Daily Standup Report schedule started - scheduled for {report_time}"
            )

    def send_daily_report(self):
        """
        Compiles and sends the daily standup report to the Slack channel.
        """
        # Push the app context before performing any database queries
        # Get list of users from the database
        users = User.query.all()

        final_message = ""

        # Compile a report for each user
        for user in users:
            final_message += f"*Daily Standup Report for <@{user.slack_user_id}>*" + "\n\n"

            final_message += "*Recently completed tasks:*" + "\n"

            recently_completed = ViewMyTasks(user.slack_user_id).get_completed_tasks()
            if recently_completed.get("blocks", []):
                for block in recently_completed["blocks"]:
                    final_message += block["text"]["text"] + "\n"
            else:
                final_message += "None" + "\n"

            final_message += "\n"

            due_soon = ViewMyTasks(user.slack_user_id).get_upcoming_tasks()

            final_message += "*Tasks due soon:*" + "\n"

            if due_soon.get("blocks", []):
                for block in due_soon["blocks"]:
                    final_message += block["text"]["text"] + "\n"
            else:
                final_message += "None" + "\n"

            final_message += "\n"

            past_due = ViewMyTasks(user.slack_user_id).get_past_due_tasks()

            # final_message += f"|{past_due}|"

            final_message += "*Tasks past due:*" + "\n"

            if past_due.get("blocks", []):
                for block in past_due["blocks"]:
                    final_message += block["text"]["text"] + "\n"
            else:
                final_message += "None" + "\n"

            final_message += "\n\n\n"

        self.post_to_slack({"text": {"text": final_message}})

    def post_to_slack(self, report_payload):
        """
        Sends the report to a Slack channel.

        :param report_payload: Payload of tasks formatted for Slack.
        """
        try:
            from app import slack_client
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