from django.urls import path

from .views import ChatView

# Define the app name for URL namespacing
app_name = "app"

# URL patterns for the 'app' app
urlpatterns = [
    # Define the URL pattern for the chat view
    # This will route the root URL ("") to the ChatView.
    # When accessed, it will use the ChatView to handle the request.
    path("", ChatView.as_view(), name="chat"),
]
