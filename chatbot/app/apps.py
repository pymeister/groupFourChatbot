from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfig):
    """
    Configuration class for the 'chatbot' app.

    This class defines the configuration for the app, including the name and
    the default field type for auto-incrementing primary keys. The class
    also makes use of Django's translation system for app labels.

    Attributes:
        - default_auto_field (str): Specifies the default type for
        auto-generated primary keys.
        - name (str): The name of the app, used for referencing the app
        in Django settings.
        - verbose_name (str): A human-readable name for the app, often
        displayed in the Django admin.
    """

    # Specifies the default type for auto-generated primary keys.
    # This will use BigAutoField
    # for new models that don't explicitly define their primary key field type.
    default_auto_field = "django.db.models.BigAutoField"

    # The full Python path to the application.
    # This is used to reference the app in settings.
    name = "chatbot.app"

    # A human-readable name for the app, used in the Django admin interface.
    # Using gettext_lazy to mark the string for language translation.
    verbose_name = _("Chatbot Application")
