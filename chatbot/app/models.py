from django.db import models

# Define the ChatMessage model to store chat interactions
class ChatMessage(models.Model):
    # Field to store the user's message
    user_message = models.TextField()
    # Field to store the bot's reponse
    bot_response = models.TextField()
    # Timestamp field that automatically records the time when each message is created 
    timestamp = models.DateTimeField(auto_now_add=True)

    # String representation of the mode instance for easy readability in the admin panel and elsewhere
    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"
