from django.contrib import admin

from .models import ChatMessage

# Define a constant for the maximum length of messages to display
MAX_MESSAGE_LENGTH = 50


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "short_user_message",
        "short_bot_response",
        "timestamp",
    )  # Display these fields in the list view
    search_fields = ("user_message", "bot_response")  # Enable search on these fields
    list_filter = ("timestamp",)  # Filter by timestamp

    @admin.display(
        description="User Message",
    )
    def short_user_message(self, obj):
        return (
            obj.user_message[:MAX_MESSAGE_LENGTH]
            if len(obj.user_message) > MAX_MESSAGE_LENGTH
            else obj.user_message
        )

    @admin.display(
        description="Bot Response",
    )
    def short_bot_response(self, obj):
        return (
            obj.bot_response[:MAX_MESSAGE_LENGTH]
            if len(obj.bot_response) > MAX_MESSAGE_LENGTH
            else obj.bot_response
        )
