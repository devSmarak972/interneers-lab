from .repository import ProductRepository, ProductCategoryRepository
class ProductService:
    """
    Service layer to handle business logic for Product operations.
    """
    @staticmethod
    def list_products():
        return ProductRepository.get_all()

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(data):
        if not data.get('brand'):
            raise ValueError("Brand is required for all products.")
        return ProductRepository.create(data)

    @staticmethod
    def update_product(product_id, data):
        product = ProductRepository.get_by_id(product_id)
        if product:
        # Ensure brand is not removed during updates
            if 'brand' in data and not data['brand']:
                raise ValueError("Brand cannot be removed from an existing product.")
            return ProductRepository.update(product, data)
        return None

    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        if product:
            ProductRepository.delete(product)
            return True
        return False

    @staticmethod
    def get_products_by_category(category_id):
        return ProductRepository.get_by_category(category_id)

    @staticmethod
    def fetch_products(filters):
        """Fetch products using filters and return JSON response."""
        products = ProductRepository.get_filtered_products(filters)
        return products
        # return [product.to_json() for product in products]

    @staticmethod
    def add_product_to_category(product_id, category_id):
        product = ProductRepository.get_by_id(product_id)
        category = ProductCategoryRepository.get_by_id(category_id)
        if product and category:
            product.category = category
            product.save()
            return product
        return None

    @staticmethod
    def remove_product_from_category(product_id):
        product = ProductRepository.get_by_id(product_id)
        if product:
            product.category = None
            product.save()
            return product
        return None
    

class ProductCategoryService:
    """
    Service layer for managing Product Categories.
    """
    @staticmethod
    def list_categories():
        return ProductCategoryRepository.get_all()

    @staticmethod
    def get_category(category_id):
        return ProductCategoryRepository.get_by_id(category_id)

    @staticmethod
    def create_category(data):
        return ProductCategoryRepository.create(data)

    @staticmethod
    def delete_category(category_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        if category:
            ProductCategoryRepository.delete(category_id)
            return True
        return False
    
    @staticmethod
    def create_or_update_category(category_data):
        """Create a new category or update an existing one."""
        category_id = category_data.get("id")

        if category_id:
            return ProductCategoryRepository.update_category(category_id, category_data)
        return ProductCategoryRepository.create_category(category_data)

