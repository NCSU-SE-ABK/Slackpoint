import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = True
    # SLACK API key:
    SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")
def check_env_variables():
    print("SQLALCHEMY_DATABASE_URI:", os.environ.get("DATABASE_URL"))
    print("SLACK_SIGNING_SECRET:", os.environ.get("SLACK_SIGNING_SECRET"))
    print("SLACK_BOT_TOKEN:", os.environ.get("SLACK_BOT_TOKEN"))
    print("VERIFICATION_TOKEN:", os.environ.get("VERIFICATION_TOKEN"))

check_env_variables()