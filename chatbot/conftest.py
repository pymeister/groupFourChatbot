import pytest

from chatbot.app.models import ChatMessage
from chatbot.app.tests.factories import (
    ChatMessageFactory,  # Ensure you import ChatMessageFactory
)
from chatbot.users.models import User
from chatbot.users.tests.factories import UserFactory

# Define constants for magic values
MAX_CONTENT_LENGTH = 1000


# Fixture to mock API_KEY for all tests
@pytest.fixture(autouse=True)
def _mock_api_key(settings):
    settings.API_KEY = "test-api-key"


# Fixture to set up media storage for tests
@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


# Fixture to create a user instance
@pytest.fixture
def user(db) -> User:
    return UserFactory()


# Fixture to create a chat message instance
@pytest.fixture
def chat_message(db) -> ChatMessage:
    return (
        ChatMessageFactory()
    )  # Ensure ChatMessageFactory is defined and correctly implemented
