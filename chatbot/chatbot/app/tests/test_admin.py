from django.contrib import admin
from django.test import TestCase, RequestFactory
from ..admin import ChatMessageAdmin
from .factories import ChatMessageFactory  # Import the factory

class TestChatMessageAdmin(TestCase):
    def setUp(self):
        # Set up a request factory and an instance of ChatMessageAdmin
        self.factory = RequestFactory()
        self.admin_site = admin.AdminSite()
        self.model_admin = ChatMessageAdmin(ChatMessageFactory._meta.model, self.admin_site)  # Use model from factory

        # Create sample chat messages using the factory
        self.chat_message1 = ChatMessageFactory(
            user_message="This is a long message that exceeds fifty characters to test truncation.",
            bot_response="This is a short response.",
            timestamp=1643723400
        )
        self.chat_message2 = ChatMessageFactory(
            user_message="Short message",
            bot_response="This is a long response that exceeds fifty characters to test truncation.",
            timestamp=1643723401
        )

    def test_list_display(self):
        # Test that list_display works correctly (e.g., truncating long user messages)
        list_display = self.model_admin.get_list_display(request=self.factory.get('/'))
        self.assertIn('user_message', list_display)
        self.assertIn('bot_response', list_display)
        self.assertIn('timestamp', list_display)

    def test_search_fields(self):
        # Test that search fields are set correctly
        search_fields = self.model_admin.get_search_fields(request=self.factory.get('/'))
        self.assertIn('user_message', search_fields)
        self.assertIn('bot_response', search_fields)

    def test_list_filter(self):
        # Test that list_filter includes 'timestamp'
        list_filter = self.model_admin.get_list_filter(request=self.factory.get('/'))
        self.assertIn('timestamp', list_filter)

    def test_short_user_message(self):
        # Test that short user messages are handled correctly
        user_message = self.model_admin.short_user_message(self.chat_message1)
        truncated_msg = "This is a long message that exceeds fifty characte"
        self.assertEqual(user_message, truncated_msg)  # Should truncate to exactly 50 characters

    def test_short_user_message_no_truncation(self):
        # Test that short user messages are not truncated
        user_message = self.model_admin.short_user_message(self.chat_message2)
        self.assertEqual(user_message, "Short message")  # No truncation needed

    def test_short_bot_response(self):
        # Test that short bot responses are handled correctly
        bot_response = self.model_admin.short_bot_response(self.chat_message2)
        truncated_resp = "This is a long response that exceeds fifty charact"
        self.assertEqual(bot_response, truncated_resp)  # Should truncate to exactly 50 characters

    def test_short_bot_response_no_truncation(self):
        # Test that short bot responses are not truncated
        bot_response = self.model_admin.short_bot_response(self.chat_message1)
        self.assertEqual(bot_response, "This is a short response.")  # No truncation needed
