import google.generativeai as ai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from requests.exceptions import RequestException

from .models import ChatMessage

# API Key for authenticating with the Generative AI service
API_KEY = settings.API_KEY

# Configure the Generative AI API with the provided API key
ai.configure(api_key=API_KEY)

# Create a new model for chat interaction using the Gemini Pro generative model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()


class ChatView(View):
    """
    ChatView handles HTTP GET and POST requests for the chat functionality.

    - GET request: Renders the chat interface (HTML page).
    - POST request: Handles user messages, sends them to the Generative AI
    model, saves the conversation to the database,
    and returns the bot's response.

    Methods:
        get: Renders the chat interface.
        post: Handles user input, gets the bot's response, saves the message,
        and returns the response in JSON format.
        get_bot_response: Sends the user message to the AI model
        and returns the response.
    """

    def get(self, request):
        """
        Handles GET requests.

        Renders the chat interface (HTML page) for the user to interact
        with the chatbot.

        Args:
            request (HttpRequest): The incoming GET request.

        Returns:
            HttpResponse: The rendered HTML page with the chat interface.
        """
        # This renders the chat interface
        return render(request, "pages/chat.html")

    def post(self, request):
        """
        Handles POST requests.

        Receives a message from the user, sends it to the bot,
        and stores the conversation in the database.

        Args:
            request (HttpRequest): The incoming POST request
            containing the user message.

        Returns:
            JsonResponse: The response from the bot returned as JSON.
        """
        # Get the user's message from the POST request
        user_message = request.POST.get("message")

        # Get the response from the bot using the user's message
        bot_response = self.get_bot_response(user_message)

        # Save the user's message and bot's response to the database
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        # Return the bot's response as JSON
        return JsonResponse({"response": bot_response})

    def get_bot_response(self, message):
        """
        Sends a message to the Generative AI model and gets the bot's response.

        Args:
            message (str): The user's message to be sent to the bot.

        Returns:
            str: The bot's response text.
        """
        try:
            # Send the user's message to the bot and get the response
            response = chat.send_message(message)
        except RequestException:
            # Handle potential API errors
            # (e.g., network issues, service downtime)
            return "There was an error processing your message. \
                Please try again later."
        else:
            # Return the bot's response text
            return response.text
