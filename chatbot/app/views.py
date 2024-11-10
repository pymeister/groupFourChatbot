import google.generativeai as ai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from requests.exceptions import RequestException

from .models import ChatMessage

# API Key
API_KEY = settings.API_KEY

# Configure the API
ai.configure(api_key=API_KEY)

# Create a new model
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()


class ChatView(View):
    def get(self, request):
        return render(request, "pages/chat.html")  # This renders chat interface

    def post(self, request):
        user_message = request.POST.get("message")
        bot_response = self.get_bot_response(user_message)

        # Save chat message to the database
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        return JsonResponse({"response": bot_response})

    def get_bot_response(self, message):
        try:
            response = chat.send_message(message)
        except RequestException:
            # Handle potential API errors
            return "There was an error processing your message. Please try again later."
        else:
            return response.text
