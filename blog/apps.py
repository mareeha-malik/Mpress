from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Blog'
    
    def ready(self):
        # App registry is ready here if needed for signal imports or initialization
        pass
