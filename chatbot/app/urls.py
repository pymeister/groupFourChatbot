from django.urls import path

from .views import ChatMessageDeleteView
from .views import ChatView

# Define the app name for URL namespacing
app_name = "app"

# URL patterns for the 'app' app
urlpatterns = [
    # Define the URL pattern for the chat view
    # This will route the root URL ("") to the ChatView.
    path("", ChatView.as_view(), name="chat"),
    # Define the URL pattern for deleting a chat message
    # This will route to ChatMessageDeleteView
    # and require a primary key (pk) for the message to delete.
    path(
        "chat/delete/<int:pk>/",
        ChatMessageDeleteView.as_view(),
        name="delete_message",
    ),
]
