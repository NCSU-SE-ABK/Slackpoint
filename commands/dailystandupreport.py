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

    def __init__(self, app, channel_id):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.app = app
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

        from app import slack_client
        with self.app.app_context():
            slack_client.chat_postMessage(
                channel=self.channel_id,
                text=f"Daily Standup Report schedule started - scheduled for {report_time}"
            )

    def get_standup_message(self, users):
        final_message = ""

        print(f"|{users}|")

        # Compile a report for each user
        for user in users:
            print(f"user: |{user}|")
            # print all info about the user
            print(f"user.slack_user_id: |{user.slack_user_id}|")
            print(f"user.user_id: |{user.user_id}|")

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

            print("attempting to get upcoming tasks")
            due_soon = ViewMyTasks(user.slack_user_id).get_upcoming_tasks()
            print("got upcoming tasks")

            final_message += "*Tasks due soon:*" + "\n"

            upcoming_tasks = ViewMyTasks(user.slack_user_id).get_upcoming_tasks()
            tasks_added = False
            for block in upcoming_tasks.get("blocks", []):
                text = block.get("text", {}).get("text")
                if text:
                    final_message += text + "\n"
                    tasks_added = True
            if not tasks_added:
                final_message += "None\n"

            final_message += "\n"

            print("attempting to get past due tasks")
            past_due = ViewMyTasks(user.slack_user_id).get_past_due_tasks()
            print("got past due tasks")

            # final_message += f"|{past_due}|"

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

            print("end loop iteration")

        print("returning: ", final_message)

        return final_message

    def send_daily_report(self):
        """
        Compiles and sends the daily standup report to the Slack channel.
        """
        # Get list of users from the database
        with self.app.app_context():
            users = User.query.all()

            final_message = self.get_standup_message(users)

            self.post_to_slack({"text": {"text": final_message}})

    def post_to_slack(self, report_payload):
        """
        Sends the report to a Slack channel.

        :param report_payload: Payload of tasks formatted for Slack.
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