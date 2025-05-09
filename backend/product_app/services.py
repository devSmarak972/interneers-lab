from product_app.repository import ProductRepository, ProductCategoryRepository
class ProductService:
    """
    Service layer to handle business logic for Product operations.
    """

    def __init__(self, product_repository=None, category_repository=None):
        self.product_repository = product_repository or ProductRepository
        self.category_repository = category_repository or ProductCategoryRepository

    def list_products(self):
        return self.product_repository.get_all()

    def get_product(self, product_id):
        return self.product_repository.get_by_id(product_id)

    def create_product(self, data):
        if not data.get('brand'):
            raise ValueError("Brand is required for all products.")
        return self.product_repository.create(data)

    def update_product(self, product_id, data):
        product = self.product_repository.get_by_id(product_id)
        if product:
            # Ensure brand is not removed during updates
            if 'brand' in data and not data['brand']:
                raise ValueError("Brand cannot be removed from an existing product.")
            return self.product_repository.update(product, data)
        return None

    def delete_product(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if product:
            self.product_repository.delete(product)
            return True
        return False

    def get_products_by_category(self, category_id):
        return self.product_repository.get_by_category(category_id)

    def fetch_products(self, filters):
        """Fetch products using filters and return JSON response."""
        products = self.product_repository.get_filtered_products(filters)
        return products

    def add_product_to_category(self, product_id, category_id):
        product = self.product_repository.get_by_id(product_id)
        category = self.category_repository.get_by_id(category_id)
        if product and category:
            product.category = category
            product.save()
            return product
        return None

    def remove_product_from_category(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if product:
            product.category = None
            product.save()
            return product
        return None
    
class ProductCategoryService:
    """
    Service layer for managing Product Categories.
    """

    def __init__(self, category_repository=None):
        self.category_repository = category_repository or ProductCategoryRepository

    def list_categories(self):
        return self.category_repository.get_all()

    def get_category(self, category_id):
        return self.category_repository.get_by_id(category_id)

    def create_category(self, data):
        existing_category = self.category_repository.get_by_title(data.get('title'))
        if existing_category:
            return existing_category  # Return the existing category if it exists
        print("Creating new category")
        return self.category_repository.create(data)

    def delete_category(self, category_id):
        category = self.category_repository.get_by_id(category_id)
        if category:
            self.category_repository.delete(category_id)
            return True
        return False

    def create_or_update_category(self, category_data):
        """Create a new category or update an existing one."""
        category_id = category_data.get("id")
        if category_id:
            return self.category_repository.update_category(category_id, category_data)
        return self.category_repository.create(category_data)