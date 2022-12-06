from copy import deepcopy

from models import *

class ViewDeadlineTasks:
    def __init__(self):
        """
        Initialise ViewTasks Class. Set progress for filtering tasks.

        :param progress: Optional Filter on tasks according to their progress.
        :type progress: float
        :raise:
        :return: ViewPoints object
        :rtype: ViewPoints object

        """
        self.payload = {"response_type": "ephemeral", "blocks": []}
