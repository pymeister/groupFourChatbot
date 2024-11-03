import factory
from factory import Faker
from ..models import ChatMessage

class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage
        django_get_or_create = ['user_message']

    user_message = Faker('sentence')  # Generate a random user message
    bot_response = Faker('sentence')  # Generate a random bot response
    timestamp = Faker('date_time')    # Generate a random timestamp
