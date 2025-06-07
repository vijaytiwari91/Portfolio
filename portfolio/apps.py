from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'
    
    def ready(self):
        """
        Method called when the app is ready.
        This is where we can run code after Django has initialized.
        """
        # Import inside ready() to avoid issues with models not being ready
        from .admin import update_admin_headers
        
        # Update the admin headers from the database
        update_admin_headers()
