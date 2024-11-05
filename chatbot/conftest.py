import pytest

from chatbot.app.models import ChatMessage
from chatbot.app.tests.factories import (
    ChatMessageFactory,  # Ensure you import ChatMessageFactory
)
from chatbot.users.models import User
from chatbot.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def chat_message(db) -> ChatMessage:  # Renamed from app to chat_message for clarity
    return (
        ChatMessageFactory()
    )  # Make sure ChatMessageFactory is defined and correctly implemented
