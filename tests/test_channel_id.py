import unittest
from unittest.mock import patch
from app import get_channel_id

class TestGetChannelId(unittest.TestCase):

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_success(self, mock_conversations_list):
        """
        Test that get_channel_id returns the correct channel ID when the channel exists.
        Mock the Slack API response to include a channel named 'general' with ID 'C123456'.
        """
        mock_conversations_list.return_value = {
            'channels': [{'name': 'general', 'id': 'C123456'}]
        }
        channel_id = get_channel_id('general')
        self.assertEqual(channel_id, 'C123456')

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_channel_not_found(self, mock_conversations_list):
        """
        Test that get_channel_id returns None when the specified channel does not exist.
        Mock the Slack API response to include a channel named 'random' but not 'general'.
        """
        mock_conversations_list.return_value = {
            'channels': [{'name': 'random', 'id': 'C654321'}]
        }
        channel_id = get_channel_id('general')
        self.assertIsNone(channel_id)

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_empty_channel_list(self, mock_conversations_list):
        """
        Test that get_channel_id returns None when the channel list is empty.
        Mock the Slack API response to return an empty list of channels.
        """
        mock_conversations_list.return_value = {
            'channels': []
        }
        channel_id = get_channel_id('general')
        self.assertIsNone(channel_id)

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_strip_hash(self, mock_conversations_list):
        """
        Test that get_channel_id correctly handles channel names with a leading hash (#).
        Mock the Slack API response to include a channel named 'general' with ID 'C123456'.
        """
        mock_conversations_list.return_value = {
            'channels': [{'name': 'general', 'id': 'C123456'}]
        }
        channel_id = get_channel_id('#general')
        self.assertEqual(channel_id, 'C123456')

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_api_error(self, mock_conversations_list):
        """
        Test that get_channel_id returns None when there is an API error.
        Mock the Slack API to raise an exception to simulate an API error.
        """
        mock_conversations_list.side_effect = Exception('API error')
        channel_id = get_channel_id('general')
        self.assertIsNone(channel_id)

if __name__ == '__main__':
    unittest.main()