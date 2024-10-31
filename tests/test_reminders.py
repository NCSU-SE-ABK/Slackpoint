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

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_long_message(self, mock_post_message):
        """Test send_reminder with a very long message."""
        long_message = 'A' * 1000
        send_reminder('C123456', long_message, 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_special_characters(self, mock_post_message):
        """Test send_reminder with a message containing special characters."""
        send_reminder('C123456', 'Test @reminder!', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_unicode_characters(self, mock_post_message):
        """Test send_reminder with a message containing unicode characters."""
        send_reminder('C123456', 'Test reminder 😊', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_empty_task_id(self, mock_post_message):
        """Test send_reminder with an empty task ID."""
        send_reminder('C123456', 'Test reminder', '')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_none_task_id(self, mock_post_message):
        """Test send_reminder with None as the task ID."""
        send_reminder('C123456', 'Test reminder', None)
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_empty_channel_id(self, mock_post_message):
        """Test send_reminder with an empty channel ID."""
        send_reminder('', 'Test reminder', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_none_channel_id(self, mock_post_message):
        """Test send_reminder with None as the channel ID."""
        send_reminder(None, 'Test reminder', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_long_task_id(self, mock_post_message):
        """Test send_reminder with a very long task ID."""
        long_task_id = 'T' * 100
        send_reminder('C123456', 'Test reminder', long_task_id)
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_special_characters_in_task_id(self, mock_post_message):
        """Test send_reminder with a task ID containing special characters."""
        send_reminder('C123456', 'Test reminder', 'T@123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_unicode_characters_in_task_id(self, mock_post_message):
        """Test send_reminder with a task ID containing unicode characters."""
        send_reminder('C123456', 'Test reminder', 'T😊123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_empty_channel_and_task_id(self, mock_post_message):
        """Test send_reminder with both empty channel ID and task ID."""
        send_reminder('', 'Test reminder', '')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_none_channel_and_task_id(self, mock_post_message):
        """Test send_reminder with both None as channel ID and task ID."""
        send_reminder(None, 'Test reminder', None)
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_long_channel_id(self, mock_post_message):
        """Test send_reminder with a very long channel ID."""
        long_channel_id = 'C' * 100
        send_reminder(long_channel_id, 'Test reminder', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_special_characters_in_channel_id(self, mock_post_message):
        """Test send_reminder with a channel ID containing special characters."""
        send_reminder('C@123456', 'Test reminder', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.conversations_list')
    def test_get_channel_id_with_numeric_name(self, mock_conversations_list):
        """Test get_channel_id with a channel name that is numeric."""
        mock_conversations_list.return_value = {'channels': [{'name': '12345', 'id': 'C123456'}]}
        channel_id = get_channel_id('12345')
        self.assertEqual(channel_id, 'C123456')

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_html_content(self, mock_post_message):
        """Test send_reminder with a message containing HTML content."""
        send_reminder('C123456', '<b>Test reminder</b>', 'T123')
        mock_post_message.assert_called_once()

    @patch('app.slack_client.chat_postMessage')
    def test_send_reminder_with_json_content(self, mock_post_message):
        """Test send_reminder with a message containing JSON content."""
        send_reminder('C123456', '{"reminder": "Test reminder"}', 'T123')
        mock_post_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()