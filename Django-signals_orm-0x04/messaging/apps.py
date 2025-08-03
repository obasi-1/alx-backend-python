# messaging/apps.py
from django.apps import AppConfig

class MessagingConfig(AppConfig):
    """
    AppConfig for the messaging application.
    Connects the signals when the app is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        """
        Import signals here to ensure they are connected
        when the Django application starts.
        """
        import messaging.signals
