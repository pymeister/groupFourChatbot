from unittest.mock import patch

import pytest
from django.http import JsonResponse
from django.urls import reverse
from requests.exceptions import RequestException

from chatbot.app.models import ChatMessage

# Define the URL for the view
CHAT_URL = reverse("app:chat")  # Replace with the actual name of your URL pattern

# Define a constant for HTTP status codes at the top of the file
HTTP_OK = 200


@pytest.mark.django_db
def test_chatview_get(client):
    # Test the GET method to ensure the correct template is rendered
    response = client.get(CHAT_URL)
    assert response.status_code == HTTP_OK
    assert "chat.html" in response.templates[0].name


@pytest.mark.django_db
def test_chatview_post(client):
    # Test the POST method to ensure chat message is created and bot responds

    # Mock the API call to the generative model
    with patch("chatbot.app.views.chat.send_message") as mock_send_message:
        mock_send_message.return_value.text = "Hello, user!"

        # Send a POST request with a message
        response = client.post(CHAT_URL, {"message": "Hi there!"})

        # Ensure the response is a JsonResponse and contains the bot's response
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert response.json().get("response") == "Hello, user!"

        # Ensure the chat message is saved to the database
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "Hi there!"
        assert chat_message.bot_response == "Hello, user!"


@pytest.mark.django_db
def test_chatview_post_error_handling(client):
    # Test the POST method with error handling when the API call fails

    # Mock the API call to raise a RequestException
    with patch("chatbot.app.views.chat.send_message", side_effect=RequestException):
        response = client.post(CHAT_URL, {"message": "Hi there!"})

        # Ensure the response is a JsonResponse and contains the error message
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert (
            response.json().get("response")
            == "There was an error processing your message. "
            "Please try again later."
        )


@pytest.mark.django_db
def test_robot_response(client):
    # Test robot's response functionality

    # Mock the API call to return a specific response
    with patch("chatbot.app.views.chat.send_message") as mock_send_message:
        mock_send_message.return_value.text = "I'm a bot, how can I help you?"

        # Send a POST request with a user message
        response = client.post(CHAT_URL, {"message": "How are you?"})

        # Ensure the response is a JsonResponse and contains the expected robot response
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert response.json().get("response") == "I'm a bot, how can I help you?"

        # Ensure the chat message was saved correctly
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "How are you?"
        assert chat_message.bot_response == "I'm a bot, how can I help you?"


@pytest.mark.django_db
def test_robot_response_error_handling(client):
    # Test the error handling for the robot's response when the API fails

    # Mock the API call to raise a RequestException
    with patch("chatbot.app.views.chat.send_message", side_effect=RequestException):
        response = client.post(CHAT_URL, {"message": "How are you?"})

        # Ensure the response is a JsonResponse and contains the error message
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert (
            response.json().get("response")
            == "There was an error processing your message. "
            "Please try again later."
        )
