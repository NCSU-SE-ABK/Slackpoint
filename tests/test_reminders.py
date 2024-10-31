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

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_empty_message(self, mock_post_message):
        """Test send_reminder with an empty message."""
        send_reminder('C123456', '', 'T123')
        mock_post_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()
