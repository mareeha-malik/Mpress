from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Accounts'
    def ready(self):
        # import signals to ensure Profile is created for new Users
        try:
            import accounts.signals  # noqa: F401
        except Exception:
            pass
