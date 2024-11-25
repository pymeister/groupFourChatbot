import pytest
from django.contrib import admin
from django.test import RequestFactory

from chatbot.app.admin import ChatMessageAdmin
from chatbot.app.models import ChatMessage
from chatbot.app.tests.factories import ChatMessageFactory


@pytest.mark.django_db
class TestChatMessageAdmin:
    def setup_method(self):
        self.admin_site = admin.AdminSite()
        self.model_admin = ChatMessageAdmin(ChatMessage, self.admin_site)
        self.factory = RequestFactory()

        # Create sample chat messages using the factory
        self.chat_message1 = ChatMessageFactory(
            user_message="This is a long message that exceeds fifty characters "
            "to test truncation.",
            bot_response="This is a short response.",
            timestamp=1643723400,
        )
        self.chat_message2 = ChatMessageFactory(
            user_message="Short message",
            bot_response="This is a long response that exceeds fifty characters "
            "to test truncation.",
            timestamp=1643723401,
        )

    def test_list_display(self):
        # Test that list_display works correctly
        list_display = self.model_admin.get_list_display(request=self.factory.get("/"))
        assert "short_user_message" in list_display
        assert "short_bot_response" in list_display
        assert "timestamp" in list_display

    def test_search_fields(self):
        # Test that search fields are set correctly
        search_fields = self.model_admin.get_search_fields(
            request=self.factory.get("/"),
        )
        assert "user_message" in search_fields
        assert "bot_response" in search_fields

    def test_list_filter(self):
        # Test that list_filter includes 'timestamp'
        list_filter = self.model_admin.get_list_filter(request=self.factory.get("/"))
        assert "timestamp" in list_filter

    def test_short_user_message(self):
        # Test that long user messages are truncated correctly
        user_message = self.model_admin.short_user_message(self.chat_message1)
        truncated_msg = "This is a long message that exceeds fifty characte"
        assert user_message == truncated_msg

    def test_short_user_message_no_truncation(self):
        # Test that short user messages are not truncated
        user_message = self.model_admin.short_user_message(self.chat_message2)
        assert user_message == "Short message"

    def test_short_bot_response(self):
        # Test that long bot responses are truncated correctly
        bot_response = self.model_admin.short_bot_response(self.chat_message2)
        truncated_resp = "This is a long response that exceeds fifty charact"
        assert (
            bot_response == truncated_resp
        )  # Should truncate to exactly 50 characters

    def test_short_bot_response_no_truncation(self):
        # Test that short bot responses are not truncated
        bot_response = self.model_admin.short_bot_response(self.chat_message1)
        assert bot_response == "This is a short response."
