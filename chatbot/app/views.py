import google.generativeai as ai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from requests.exceptions import RequestException

from .models import ChatMessage

# API Key from Django Settings
API_KEY = settings.API_KEY

# Configure the Google Generative AI API with the API key
ai.configure(api_key=API_KEY)

# Create a new generative AI model instance: Start a chat session with the AI model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()


class ChatView(View):
    # Handle GET requests to render the chat interface page: Render the chat interface HTML page
    def get(self, request):
        return render(request, "pages/chat.html") 

    # Handle POST requests to process chat messages: Get the user's message from POST request and bot's response for message
    def post(self, request):
        user_message = request.POST.get("message")
        bot_response = self.get_bot_response(user_message)

        # Save chat message to the database, including user message and bot response
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        # Return the bot's response as JSON data
        return JsonResponse({"response": bot_response})

    # Helper method to get the bot's response for a given user message: Send message to the AI model & get response
    def get_bot_response(self, message):
        try:
            response = chat.send_message(message)
        except RequestException:
            # Handle potential API errors that might occur during the message send process
            return "There was an error processing your message. Please try again later."
        else:
            return response.text
