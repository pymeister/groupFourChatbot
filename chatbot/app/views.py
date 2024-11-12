import google.generativeai as ai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from requests.exceptions import RequestException

from .models import ChatMessage

# API Key: Gets the API key from Django settings for accessing the Google AI API
API_KEY = settings.API_KEY

# Configure the API: Uses the API key to configure the generative AI service
ai.configure(api_key=API_KEY)

# Create a new model: Instantiates the generative model "gemini-pro" and starts a new chat session using the model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Defines the ChatView class that handles requests/response for the chat page
class ChatView(View):
    def get(self, request):
        # Renders the chat interface template when the user accesses the chat page: Renders the chat.html page for the user interface
        return render(request, "pages/chat.html") 

    def post(self, request):
        # Handles the POST request when the user sends a message: Retrieves the user's message from the POST data and gets the response from the bot using the message.
        user_message = request.POST.get("message")
        bot_response = self.get_bot_response(user_message)

        # Save both user's message and the bot's response to to the database for later reference: Create a new ChattMessage in the datbase.
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        # Return the bot's response as a JSON response: Send a JSON response containing the bot's response.
        return JsonResponse({"response": bot_response})

    def get_bot_response(self, message):
        try:
            # Send the user's message to the AI model and get the response: Send the message to the AI chat and get the response
            response = chat.send_message(message)
        except RequestException:
            # Handle potential API errors, to include things such as network issues or server unavailability: Return a friendly error message
            return "There was an error processing your message. Please try again later."
        else:
            # If 0 errors, return the text of the response from the AI model: Return the generated response text from the AI model
            return response.text
