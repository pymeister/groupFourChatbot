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
        assert (
            response.json().get("response")
            == "I am not designed to answer that. Can you please ask a medical-related question?"
        )

        # Ensure the chat message is saved to the database
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "Hi there!"
        assert chat_message.bot_response == (
            "I am not designed to answer that. Can you please ask a medical-related question?"
        )


@pytest.mark.django_db
def test_chatview_post_with_medical_terms(client):
    # Test the POST method with medical-related terms in the message

    # Mock the API call to the generative model
    with patch("chatbot.app.views.chat.send_message") as mock_send_message:
        mock_send_message.return_value.text = (
            "Hello, user! I'm here to assist with medical queries."
        )

        # Send a POST request with a medical-related message
        response = client.post(
            CHAT_URL,
            {"message": "What are the symptoms of diabetes?"},
        )

        # Ensure the response is a JsonResponse and contains the bot's response
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert response.json().get("response") == (
            "Hello, user! I'm here to assist with medical queries."
        )

        # Ensure the chat message is saved to the database
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "What are the symptoms of diabetes?"
        assert chat_message.bot_response == (
            "Hello, user! I'm here to assist with medical queries."
        )


@pytest.mark.django_db
def test_chatview_post_with_no_medical_terms(client):
    # Test the POST method with no medical-related terms in the message

    # Mock the API call to the generative model
    with patch("chatbot.app.views.chat.send_message") as mock_send_message:
        mock_send_message.return_value.text = (
            "Hello, user! I'm here to assist with medical queries."
        )

        # Send a POST request with a message containing no medical-related terms
        response = client.post(CHAT_URL, {"message": "How are you?"})

        # Ensure the response is a JsonResponse and contains the bot's response
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert (
            response.json().get("response")
            == "I am not designed to answer that. Can you please ask a medical-related question?"
        )

        # Ensure the chat message is saved to the database
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "How are you?"
        assert chat_message.bot_response == (
            "I am not designed to answer that. Can you please ask a medical-related question?"
        )


@pytest.mark.django_db
def test_bot_error_handling(client):
    """
    Test that the bot handles API errors gracefully (e.g., network issue).
    """
    # Simulate an API failure by raising a RequestException
    with patch(
        "chatbot.app.views.chat.send_message",
        side_effect=RequestException("Network error"),
    ):
        response = client.post(
            reverse("app:chat"),
            data={"message": "What is a headache?"},
        )

        # Ensure the error handling message is returned
        assert response.status_code == HTTP_OK
        assert response.json()["response"] == (
            "There was an error processing your message. Please try again later."
        )


@pytest.mark.django_db
def test_chatview_post_with_bye_message(client):
    # Test that the bot responds with 'Goodbye!' when 'bye' is sent.

    # Mock the API call to the generative model
    with patch("chatbot.app.views.chat.send_message") as mock_send_message:
        mock_send_message.return_value.text = "Goodbye!"

        # Send a POST request with the 'bye' message
        response = client.post(CHAT_URL, {"message": "bye"})

        # Ensure the response is a JsonResponse and contains the bot's response
        assert isinstance(response, JsonResponse)
        assert response.status_code == HTTP_OK
        assert response.json().get("response") == "Goodbye!"

        # Ensure the chat message is saved to the database
        chat_message = ChatMessage.objects.last()
        assert chat_message.user_message == "bye"
        assert chat_message.bot_response == "Goodbye!"


@pytest.mark.django_db
def test_message_saved_in_db_with_no_medical_terms(client):
    """
    Test that the user's message and bot's response are saved in the database
    when no medical terms are found.
    """
    # Send a message with no medical-related terms
    client.post(CHAT_URL, data={"message": "Hello!"})

    # Check that the message and bot response are stored in the database
    assert ChatMessage.objects.count() == 1  # Ensure one message is saved

    chat_message = ChatMessage.objects.first()
    assert chat_message.user_message == "Hello!"
    assert chat_message.bot_response == (
        "I am not designed to answer that. Can you please ask a medical-related question?"
    )


@pytest.mark.django_db
def test_message_saved_in_db_with_bye_message(client):
    """
    Test that the 'bye' message and bot's response are saved in the database.
    """
    # Send the 'bye' message
    client.post(CHAT_URL, data={"message": "bye"})

    # Check that the message and bot response are stored in the database
    assert ChatMessage.objects.count() == 1  # Ensure one message is saved

    chat_message = ChatMessage.objects.first()
    assert chat_message.user_message == "bye"
    assert chat_message.bot_response == "Goodbye!"
