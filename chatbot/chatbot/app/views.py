from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import ChatMessage

class ChatView(View):
    def get(self, request):
        return render(request, 'pages/chat.html')  # This renders chat interface

    def post(self, request):
        user_message = request.POST.get('message')
        bot_response = self.get_bot_response(user_message)  # This gets bot response logic

        # Save chat message to the database
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)

        return JsonResponse({'response': bot_response})

    def get_bot_response(self, message):
        # Here is where the NLP logic should be implemented
        return f"You said: {message}"  # This is a simple echo for demo purposes. It should be removed when creating the logic

