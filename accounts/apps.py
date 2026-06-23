from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Accounts'
    
    def ready(self):
        # Import signals here so they are registered when the app registry is ready.
        # This prevents "app_label not declared" errors during test discovery.
        from . import signals  # noqa: F401
