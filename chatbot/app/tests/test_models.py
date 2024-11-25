import pytest
from django.utils import timezone

from chatbot.app.models import ChatMessage


@pytest.mark.django_db
def test_chat_message_creation():
    # Create a ChatMessage instance
    user_message = "Hello, bot!"
    bot_response = "Hello, user!"
    chat_message = ChatMessage.objects.create(
        user_message=user_message,
        bot_response=bot_response,
    )

    # Check if the ChatMessage was created
    assert ChatMessage.objects.count() == 1
    assert chat_message.user_message == user_message
    assert chat_message.bot_response == bot_response
    assert isinstance(chat_message.timestamp, timezone.datetime)


@pytest.mark.django_db
def test_chat_message_str_method():
    # Create a ChatMessage instance
    user_message = "Hi!"
    bot_response = "Hello!"
    chat_message = ChatMessage.objects.create(
        user_message=user_message,
        bot_response=bot_response,
    )

    # Test the __str__ method
    expected_str = f"User: {user_message} | Bot: {bot_response}"
    assert str(chat_message) == expected_str
