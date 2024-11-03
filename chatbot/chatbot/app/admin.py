# chatbot/app/admin.py
from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'bot_response', 'timestamp')  # Display these fields in the list view
    search_fields = ('user_message', 'bot_response')              # Enable search on these fields
    list_filter = ('timestamp',)                                  # Filter by timestamp

    def short_user_message(self, obj):
        return obj.user_message[:50] if len(obj.user_message) > 50 else obj.user_message
    short_user_message.short_description = 'User Message'

    def short_bot_response(self, obj):
        return obj.bot_response[:50] if len(obj.bot_response) > 50 else obj.bot_response
    short_bot_response.short_description = 'Bot Response'
