from copy import deepcopy

from models import *
class ViewMyTasks:
    """
    This class is used to view a list of tasks on the slack bot as per the user they have been assigned to
    """

    base_point_block_format = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ">SP-{id} ({points} SlackPoints) {description} [Deadline: {deadline}]",
        },
    }

    def __init__(self, user_id):
        """
        Initialise ViewTasks Class. Set progress for filtering tasks.

        :param progress: Optional Filter on tasks according to their progress.
        :type progress: float
        :raise:
        :return: ViewPoints object
        :rtype: ViewPoints object

        """
        self.user_id = user_id
        self.payload = {"response_type": "ephemeral", "blocks": []}
