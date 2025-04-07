import pytest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(0, parent_dir)
from services import ProductService

@pytest.fixture
def mock_repos():
    """
    Fixture to provide mock repositories for products and categories.
    """
    return {
        "product_repo": MagicMock(),
        "category_repo": MagicMock()
    }

@pytest.fixture
def service(mock_repos):
    """
    Fixture to provide a ProductService instance with mock repositories.
    """
    return ProductService(
        product_repository=mock_repos["product_repo"],
        category_repository=mock_repos["category_repo"]
    )

def test_create_product_success(service, mock_repos):
    """
    Test creating a product successfully.
    Ensures the product is created and the repository's create method is called.
    """
    mock_product = {"name": "Pen", "brand": "Cello"}
    mock_repos["product_repo"].create.return_value = mock_product

    result = service.create_product(mock_product)

    assert result == mock_product
    mock_repos["product_repo"].create.assert_called_once_with(mock_product)

def test_create_product_without_brand_raises_error(service):
    """
    Test creating a product without a brand.
    Ensures a ValueError is raised when the brand is missing.
    """
    data = {"name": "NoBrand"}
    with pytest.raises(ValueError, match="Brand is required"):
        service.create_product(data)

def test_list_products(service, mock_repos):
    """
    Test listing all products.
    Ensures the repository's get_all method is called and returns the correct products.
    """
    mock_repos["product_repo"].get_all.return_value = ["product1", "product2"]
    result = service.list_products()
    assert result == ["product1", "product2"]
    mock_repos["product_repo"].get_all.assert_called_once()

def test_get_product(service, mock_repos):
    """
    Test retrieving a product by ID.
    Ensures the repository's get_by_id method is called and returns the correct product.
    """
    mock_product = {"id": "123"}
    mock_repos["product_repo"].get_by_id.return_value = mock_product
    result = service.get_product("123")
    assert result == mock_product
    mock_repos["product_repo"].get_by_id.assert_called_once_with("123")

def test_update_product_success(service, mock_repos):
    """
    Test updating a product successfully.
    Ensures the repository's update method is called with the correct arguments.
    """
    existing_product = {"id": "1", "brand": "Cello"}
    update_data = {"name": "Updated", "brand": "Cello"}
    mock_repos["product_repo"].get_by_id.return_value = existing_product
    mock_repos["product_repo"].update.return_value = "updated_product"

    result = service.update_product("1", update_data)

    assert result == "updated_product"
    mock_repos["product_repo"].get_by_id.assert_called_once_with("1")
    mock_repos["product_repo"].update.assert_called_once_with(existing_product, update_data)

def test_update_product_invalid_brand(service, mock_repos):
    """
    Test updating a product with an invalid brand.
    Ensures a ValueError is raised when the brand is removed.
    """
    product = {"id": "1", "brand": "Cello"}
    mock_repos["product_repo"].get_by_id.return_value = product
    with pytest.raises(ValueError, match="Brand cannot be removed"):
        service.update_product("1", {"brand": ""})

def test_update_product_not_found(service, mock_repos):
    """
    Test updating a product that does not exist.
    Ensures None is returned when the product is not found.
    """
    mock_repos["product_repo"].get_by_id.return_value = None
    result = service.update_product("123", {"name": "test"})
    assert result is None

def test_delete_product_success(service, mock_repos):
    """
    Test deleting a product successfully.
    Ensures the repository's delete method is called with the correct product.
    """
    mock_product = MagicMock()
    mock_repos["product_repo"].get_by_id.return_value = mock_product

    result = service.delete_product("123")

    assert result is True
    mock_repos["product_repo"].delete.assert_called_once_with(mock_product)

def test_delete_product_not_found(service, mock_repos):
    """
    Test deleting a product that does not exist.
    Ensures False is returned when the product is not found.
    """
    mock_repos["product_repo"].get_by_id.return_value = None
    result = service.delete_product("123")
    assert result is False

def test_get_products_by_category(service, mock_repos):
    """
    Test retrieving products by category.
    Ensures the repository's get_by_category method is called with the correct category ID.
    """
    mock_repos["product_repo"].get_by_category.return_value = ["prod1"]
    result = service.get_products_by_category("cat123")
    assert result == ["prod1"]
    mock_repos["product_repo"].get_by_category.assert_called_once_with("cat123")

def test_fetch_products_with_filters(service, mock_repos):
    """
    Test fetching products with filters.
    Ensures the repository's get_filtered_products method is called with the correct filters.
    """
    filters = {"brand": "Cello"}
    mock_repos["product_repo"].get_filtered_products.return_value = ["filtered_prod"]
    result = service.fetch_products(filters)
    assert result == ["filtered_prod"]
    mock_repos["product_repo"].get_filtered_products.assert_called_once_with(filters)

def test_add_product_to_category_success(service, mock_repos):
    """
    Test adding a product to a category successfully.
    Ensures the product's category is updated and saved.
    """
    product = MagicMock()
    category = MagicMock()
    mock_repos["product_repo"].get_by_id.return_value = product
    mock_repos["category_repo"].get_by_id.return_value = category

    result = service.add_product_to_category("p1", "c1")

    assert result == product
    assert product.category == category
    product.save.assert_called_once()

def test_add_product_to_category_failure(service, mock_repos):
    """
    Test adding a product to a category when either the product or category is not found.
    Ensures None is returned.
    """
    mock_repos["product_repo"].get_by_id.return_value = None
    mock_repos["category_repo"].get_by_id.return_value = None

    result = service.add_product_to_category("p1", "c1")

    assert result is None

def test_remove_product_from_category_success(service, mock_repos):
    """
    Test removing a product from a category successfully.
    Ensures the product's category is set to None and saved.
    """
    product = MagicMock()
    mock_repos["product_repo"].get_by_id.return_value = product

    result = service.remove_product_from_category("p1")

    assert result == product
    assert product.category is None
    product.save.assert_called_once()

def test_remove_product_from_category_not_found(service, mock_repos):
    """
    Test removing a product from a category when the product is not found.
    Ensures None is returned.
    """
    mock_repos["product_repo"].get_by_id.return_value = None
    result = service.remove_product_from_category("p1")
    assert result is None