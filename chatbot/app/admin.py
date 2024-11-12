from django.contrib import admin

from .models import ChatMessage

# Define a constant for the maximum length of messages displayed in the admin list view
MAX_MESSAGE_LENGTH = 50

# Register the ChatMessage model in the admin interface with custom display options
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view for ChatMessage objects
    list_display = (
        # Short version of user message
        "short_user_message",
        # Short version of bot response
        "short_bot_response",
        # Display timestamp of each chat message
        "timestamp",
    )  # Display these fields in the list view
    search_fields = ("user_message", "bot_response")  # Enable search on these fields
    list_filter = ("timestamp",)  # Filter by timestamp

    # Define a method to display a shortened user message in the admin
    @admin.display(
        description="User Message",
    )
    def short_user_message(self, obj):
        # Return a truncated version of user_message if it exceeds MAX_MESSAGE_LENGTH
        return (
            obj.user_message[:MAX_MESSAGE_LENGTH]
            if len(obj.user_message) > MAX_MESSAGE_LENGTH
            else obj.user_message
        )

    # Define a method to display a shortened bot response in the admin
    @admin.display(
        description="Bot Response",
    )
    def short_bot_response(self, obj):
        # Return a truncated version of bot_response if it exceeds MAX_MESSAGE_LENGTH
        return (
            obj.bot_response[:MAX_MESSAGE_LENGTH]
            if len(obj.bot_response) > MAX_MESSAGE_LENGTH
            else obj.bot_response
        )
