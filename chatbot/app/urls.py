from django.urls import path

from .views import ChatView

app_name = "app"

urlpatterns = [
    path("", ChatView.as_view(), name="chat"),
]
