import os
import django

# Set up Django settings to run the script independently
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from product_app.models import Product, ProductCategory  # Adjust based on your project structure
from product_app.repository import ProductCategoryRepository

def migrate_products():
    """Ensure all products have valid categories by assigning a default category."""
    
    # Get or create the default category
    # print(ProductCategory.objects)
    default_category, created = ProductCategoryRepository.get_or_create(
        title="Uncategorized",
        description="Default category for unclassified products"
    )

    # Find products without a category
    products_without_category = Product.objects.filter(category=None)
    print(f"Found {products_without_category.count()} products without a category.")

    # Update them with the default category
    updated_count = products_without_category.update(category=default_category)
    print(f"Updated {updated_count} products with the default category '{default_category.title}'.")

if __name__ == "__main__":
    migrate_products()
    print("Product category migration completed successfully.")
