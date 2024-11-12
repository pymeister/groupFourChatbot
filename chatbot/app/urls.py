from django.urls import path

from .views import ChatView

# Namespace for this app's URL's
app_name = "app"

# Define URL Patterns for the app
urlpatterns = [
    # URL pattern for the chat page; directs the root URL to the ChatView: Calls ChatView when the base URL is accessed
    path("", ChatView.as_view(), name="chat"),
]
