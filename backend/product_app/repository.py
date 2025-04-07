from product_app.models import Product, ProductCategory
from datetime import datetime
from product_app.models import Product, ProductCategory  # Assuming models are defined properly
from bson import ObjectId
from mongoengine.queryset.visitor import Q

class ProductRepository:
    """
    Repository layer to abstract database operations for Products.
    """
    @staticmethod
    def get_all():

        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.objects(id=product_id).first()

    @staticmethod
    def create(data):
        category_id = data.get('category')
        if category_id:
            category = ProductCategory.objects(id=category_id).first()
            if not category:
                # If the provided category is invalid, set to default "Uncategorized"
                category = ProductCategory.objects(title="Uncategorized").first()
                if not category:
                    category = ProductCategory(title="Uncategorized", description="Default category").save()
                data['category'] = category
        else:
            # If no category is provided, set to default "Uncategorized"
            category = ProductCategory.objects(title="Uncategorized").first()
            if not category:
                category = ProductCategory(title="Uncategorized", description="Default category").save()
            data['category'] = category

        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    @staticmethod
    def delete(product):
        product.delete()

    @staticmethod
    def get_by_category(category_id):
        return Product.objects(category=category_id)
    

        
    @staticmethod
    def get_filtered_products(filters):
        """Fetch products based on given filters."""
        query = Q()

        # Filter by categories
        if "categories" in filters:
            query &= Q(category__in=filters["categories"])

        # Filter by price range
        if "min_price" in filters:
            query &= Q(price__gte=filters["min_price"])
        if "max_price" in filters:
            query &= Q(price__lte=filters["max_price"])

        # Filter by brand
        if "brand" in filters:
            query &= Q(brand__icontains=filters["brand"])

        # Search query across product title and description
        if "search" in filters:
            query &= (Q(name__icontains=filters["search"]) | Q(description__icontains=filters["search"]))
        print(query,"query")
        return Product.objects(query)
    


class ProductCategoryRepository:
    """
    Repository layer to abstract database operations for Product Categories.
    """
    @staticmethod
    def get_all():
        return ProductCategory.objects.all()

    @staticmethod
    def get_by_id(category_id):
        return ProductCategory.objects(id=category_id).first()

    @staticmethod
    def create(data):
        category = ProductCategory(**data)
        category.save()
        return category


    @staticmethod
    def update(category_id, update_data):
        """Update an existing category."""
        category = ProductCategoryRepository.get_by_id(category_id)
        if category:
            category.update(**update_data)
            category.reload()
            return category
        return None

    @staticmethod
    def delete(category_id):
        """Delete a category and reassign products to a default category."""
        category = ProductCategoryRepository.get_by_id(category_id)
        if category:
            default_category = ProductCategoryRepository.get_default_category()
            Product.objects(category=category).update(set__category=default_category)
            category.delete()
            return True
        return False


    @staticmethod
    def get_default_category():
        """Fetch or create a default 'Uncategorized' category."""
        default_category = ProductCategory.objects(title="Uncategorized").first()
        if not default_category:
            default_category = ProductCategory(title="Uncategorized", description="Default category").save()
        return default_category
    
    @staticmethod
    def get_or_create(title: str, description: str = "Default category") -> ProductCategory:
        """
        Retrieves a category by title if it exists; otherwise, creates a new one.

        :param title: The title of the category.
        :param description: The description (default if creating a new category).
        :return: The retrieved or newly created ProductCategory object.
        """
        category = ProductCategory.objects(title=title).first()  # Check if it exists
        if not category:
            category = ProductCategory(title=title, description=description)
            category.save()  # Create a new category
            print(f"Created new category: {title}")
            return category,True
        else:
            print(f"Found existing category: {title}")
            return category,False
    @staticmethod
    def get_by_title(title):
        """
        Fetch a ProductCategory by its title.
        """
        return ProductCategory.objects(title=title).first()

