from django.apps import AppConfig

class ProductAppConfig(AppConfig):
    name = 'product_app'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # Import and run the validation script
        from .startup import validate_product_references
        validate_product_references()