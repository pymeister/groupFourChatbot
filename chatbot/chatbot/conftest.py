import pytest
from chatbot.users.models import User
from chatbot.users.tests.factories import UserFactory
from chatbot.app.models import ChatMessage

@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath

@pytest.fixture
def user(db) -> User:
    return UserFactory()

@pytest.fixture
def app(db) -> ChatMessage:
    return ChatMessageFactory()
