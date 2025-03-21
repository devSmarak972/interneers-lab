from mongoengine import connect
from .models import Product, ProductCategory
from mongoengine import DoesNotExist, ValidationError
from .repository import ProductCategoryRepository
def validate_product_references():
    """
    Ensures all Product documents have a valid category reference.
    If a category is missing, assigns a default category instead of deleting the product.
    """
    # Get or create a default category
    # default_category = ProductCategory.objects(title="Uncategorized").first()
    # if not default_category:
    #     default_category = ProductCategory(title="Uncategorized", description="Default category").save()
    default_category = ProductCategoryRepository.get_default_category()
    for product in Product.objects:
        try:
            # If the category is missing or the reference is invalid, assign the default category
            if not product.category or not ProductCategory.objects(id=product.category.id).first():
                print(f"Invalid category reference for Product {product.id}. Assigning default category.")

                product.category = default_category  # Assign default
                product.save()
                print(f"Assigned default category to Product {product.id}")

            # else:
                # print(f"Product {product.id} has a valid category.")
        except DoesNotExist:
            print(f"Product {product.id} references a non-existent category. Updating to default category.")

            # Assign the default category and update the database
            product.update(set__category=default_category)
            print(f"Updated Product {product.id} with default category {default_category.id}")

        except ValidationError as e:
            print(f"Validation error for Product {product.id}: {e}")

    print("Finished validating and updating product references...")