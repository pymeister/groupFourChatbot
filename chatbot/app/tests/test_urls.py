import pytest
from django.urls import resolve
from django.urls import reverse

# Define a constant for HTTP status codes at the top of the file
HTTP_OK = 200


@pytest.mark.django_db
def test_chat_url_resolves_to_chat_view():
    url = reverse("app:chat")  # Use reverse to get the URL for the chat view
    assert (
        resolve(url).view_name == "app:chat"
    )  # Check that the resolved view name is correct


@pytest.mark.django_db
def test_chat_url_accessibility(client):
    url = reverse("app:chat")  # Use reverse to get the URL for the chat view
    response = client.get(url)  # Make a GET request to the URL
    assert (
        response.status_code == HTTP_OK
    )  # Check that the response status code is 200 (OK)
