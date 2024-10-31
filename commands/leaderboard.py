from copy import deepcopy
from models import *
from sqlalchemy import desc, func


class Leaderboard:
    """
    This class generates a leaderboard, displaying the top point scorers based on completed tasks.

    **Why**: Useful for tracking task completion in a gamified environment, allowing users to see where they stand
    compared to others and encouraging active participation in completing tasks.

    **How**: Common usage examples:
    1. `Leaderboard.view_leaderboard(top_k=5)`: Retrieve the top 5 users based on points.
    """

    base_leaderboard_block_format = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "{pos}. <@{userid}> has {points} points!"},
    }

    def __init__(self):
        """
        Initializes the Leaderboard object with a payload template for response formatting.

        **Why**: Sets up a structured payload format compatible with Slack, enabling easy message display.
        **How**: Example usage -
        ```
        leaderboard = Leaderboard()
        ```
        """
        self.payload = {"response_type": "ephemeral", "blocks": []}

    def view_leaderboard(self, top_k: int = 5) -> dict:
        """
        Retrieves and formats the leaderboard with the top K users by points from completed tasks.

        :param top_k: Number of top users to display on the leaderboard, default is 5.
        :type top_k: int
        :return: Payload containing leaderboard information for the top K users.
        :rtype: dict[str, Any]

        **Why**: Displays high-performing users in a structured format, motivating users to stay engaged by
        highlighting achievements and fostering a sense of competition.
        **How**: Example usage -
        ```
        top_users = leaderboard.view_leaderboard(top_k=10)
        ```
        """
        top_5_leaderboard = (
            Assignment.query.join(Task)
            .join(User)
            .with_entities(
                User.user_id,
                User.slack_user_id,
                func.sum(Task.points).label("total_points"),
            )
            .filter(Assignment.progress == 1)
            .group_by(User.user_id)
            .order_by(desc("total_points"))[:top_k]
        )

        # Parse leaderboard data
        count = 0
        for user in top_5_leaderboard:
            count += 1
            point = deepcopy(self.base_leaderboard_block_format)
            point["text"]["text"] = point["text"]["text"].format(
                pos=count, userid=user.slack_user_id, points=user.total_points
            )
            self.payload["blocks"].append(point)
        if not self.payload["blocks"]:
            self.payload["blocks"].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ">Looks like the competition hasn't started yet :(",
                    },
                }
            )
        return self.payload
