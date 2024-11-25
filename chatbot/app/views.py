import google.generativeai as ai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView
from requests.exceptions import RequestException

from .medical_words import search_words
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
    """

    def get(self, request):
        """
        Handles GET requests.
        Renders the chat interface (HTML page) and displays chat history.
        """
        # Retrieve all chat messages from the database
        messages = ChatMessage.objects.all()

        # Render the chat interface and pass the messages to the template
        return render(request, "pages/chat.html", {"messages": messages})

    def post(self, request):
        """
        Handles POST requests.
        Receives a message from the user, sends it to the bot if
        medical-related terms are found, and stores the conversation in the database.
        """
        # Get the user's message from the POST request
        user_message = request.POST.get("message")

        # Search for medical-related words in the user's message
        found_words = [word for word in search_words if word in user_message]

        if found_words:
            bot_response = self.get_bot_response(user_message)
        # If the message is 'bye', respond accordingly
        elif user_message.lower() == "bye":
            bot_response = "Goodbye!"
        else:
            # If no relevant words are found, prompt for a medical-related question
            bot_response = """I am not designed to answer that. Can you please ask a
            medical-related question?"""

        # Save the user's message and bot's response to the database
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        # Return the bot's response as JSON
        return JsonResponse({"response": bot_response})

    def get_bot_response(self, message):
        """
        Sends a message to the Generative AI model and gets the bot's response.
        """
        try:
            # Send the user's message to the bot and get the response
            response = chat.send_message(message)
        except RequestException:
            # Handle potential API errors (e.g., network issues, service downtime)
            return "There was an error processing your message. Please try again later."
        else:
            return response.text


class ChatMessageDeleteView(DeleteView):
    """
    View for deleting a chat message.
    """

    model = ChatMessage
    template_name = "pages/delete_chat_message.html"
    success_url = reverse_lazy("app:chat")  # Redirect back to chat page after deletion
