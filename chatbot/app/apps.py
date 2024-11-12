from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Define the configuration class for the app
class AppConfig(AppConfig):
    # Set the default field type for auto-generated primary keys
    default_auto_field = "django.db.models.BigAutoField"
    # Define the full Python path to the app
    name = "chatbot.app"
    # Human-Readable name for the app, wrapped in translation utility for localization
    verbose_name = _("Application")
