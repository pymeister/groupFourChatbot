from django.contrib import admin

from .models import ChatMessage

# Define a constant for the maximum length of messages to display
MAX_MESSAGE_LENGTH = 50


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ChatMessage model.

    This class customizes the admin interface for the ChatMessage model to
    improve the user experience. It defines which fields to display, enables
    search functionality, and provides filtering options. It also customizes
    how the user message and bot response are displayed by truncating long
    messages to a manageable length.

    Attributes:
        list_display (tuple): Fields to be displayed in the list view.
        search_fields (tuple): Fields to be searchable in the admin.
        list_filter (tuple): Fields to filter the list view by.
    """

    # Defines fields displayed in the list view of the admin interface.
    list_display = (
        "short_user_message",  # Displays truncated user's message
        "short_bot_response",  # Displays truncated bot's response
        "timestamp",  # Display the timestamp of when the message was created
    )

    # Enable searching by the user message and bot response.
    search_fields = ("user_message", "bot_response")

    # Enable filtering by the timestamp of when the message was created.
    list_filter = ("timestamp",)

    @admin.display(
        description="User Message",  # Set the column header for this field
    )
    def short_user_message(self, obj):
        """
        Return a truncated version of the user message for display in the admin
        list view.

        If the user message is longer than the maximum allowed length, it will
        be truncated. Otherwise, the full message will be displayed.

        Args:
            obj (ChatMessage): The instance of the ChatMessage model
            being displayed.

        Returns:
            str: The truncated or full user message.
        """
        return (
            obj.user_message[:MAX_MESSAGE_LENGTH]
            if len(obj.user_message) > MAX_MESSAGE_LENGTH
            else obj.user_message
        )

    @admin.display(
        description="Bot Response",  # Set the column header for this field
    )
    def short_bot_response(self, obj):
        """
        Return a truncated version of the bot response for display in the
        admin list view.

        If the bot response is longer than the maximum allowed length,
        it will be truncated. Otherwise, the full response will be displayed.

        Args:
            obj (ChatMessage): The instance of the ChatMessage model
            being displayed.

        Returns:
            str: The truncated or full bot response.
        """
        return (
            obj.bot_response[:MAX_MESSAGE_LENGTH]
            if len(obj.bot_response) > MAX_MESSAGE_LENGTH
            else obj.bot_response
        )
