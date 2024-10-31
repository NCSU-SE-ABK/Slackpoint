import unittest
from unittest.mock import patch, MagicMock
from app import get_channel_id, send_reminder, app


class TestAppFunctions(unittest.TestCase):

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_with_special_characters(self, mock_conversations_list):
        """Test get_channel_id with a channel name containing special characters."""
        mock_conversations_list.return_value = {'channels': [{'name': 'general', 'id': 'C123456'}]}
        channel_id = get_channel_id('general!')
        self.assertIsNone(channel_id)

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_with_empty_string(self, mock_conversations_list):
        """Test get_channel_id with an empty string as the channel name."""
        mock_conversations_list.return_value = {'channels': [{'name': 'general', 'id': 'C123456'}]}
        channel_id = get_channel_id('')
        self.assertIsNone(channel_id)


if __name__ == '__main__':
    unittest.main()
