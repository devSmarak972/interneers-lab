import pytest
from unittest.mock import MagicMock
import sys
import os
parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(0, parent_dir)
from services import ProductService, ProductCategoryService

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
def product_service(mock_repos):
    """
    Fixture to provide a ProductService instance with mock repositories.
    """
    return ProductService(
        product_repository=mock_repos["product_repo"],
        category_repository=mock_repos["category_repo"]
    )

@pytest.fixture
def category_service(mock_repos):
    """
    Fixture to provide a ProductCategoryService instance with mock repositories.
    """
    return ProductCategoryService(
        category_repository=mock_repos["category_repo"]
    )

# Tests for ProductCategoryService
def test_create_category_success(category_service, mock_repos):
    """
    Test creating a category successfully.
    Ensures the category is created and the repository's create method is called.
    """
    mock_category = {"title": "Food", "description": "Essentials"}
    mock_repos["category_repo"].create.return_value = mock_category
    mock_repos["category_repo"].get_by_title.return_value = None

    result = category_service.create_category(mock_category)
    assert result == mock_category
    mock_repos["category_repo"].create.assert_called_once_with(mock_category)

def test_create_category_existing(category_service, mock_repos):
    """
    Test creating a category that already exists.
    Ensures the existing category is returned and no new category is created.
    """
    existing_category = {"title": "Food", "description": "Essentials"}
    mock_repos["category_repo"].get_by_title.return_value = existing_category

    result = category_service.create_category({"title": "Food", "description": "Essentials"})

    assert result == existing_category
    mock_repos["category_repo"].get_by_title.assert_called_once_with("Food")
    mock_repos["category_repo"].create.assert_not_called()

def test_list_categories(category_service, mock_repos):
    """
    Test listing all categories.
    Ensures the repository's get_all method is called and returns the correct categories.
    """
    mock_repos["category_repo"].get_all.return_value = ["category1", "category2"]
    result = category_service.list_categories()
    assert result == ["category1", "category2"]
    mock_repos["category_repo"].get_all.assert_called_once()

def test_get_category_success(category_service, mock_repos):
    """
    Test retrieving a category by ID successfully.
    Ensures the repository's get_by_id method is called and returns the correct category.
    """
    mock_category = {"id": "123", "title": "Food"}
    mock_repos["category_repo"].get_by_id.return_value = mock_category

    result = category_service.get_category("123")

    assert result == mock_category
    mock_repos["category_repo"].get_by_id.assert_called_once_with("123")

def test_get_category_not_found(category_service, mock_repos):
    """
    Test retrieving a category that does not exist.
    Ensures None is returned when the category is not found.
    """
    mock_repos["category_repo"].get_by_id.return_value = None

    result = category_service.get_category("123")

    assert result is None
    mock_repos["category_repo"].get_by_id.assert_called_once_with("123")

def test_delete_category_success(category_service, mock_repos):
    """
    Test deleting a category successfully.
    Ensures the repository's delete method is called with the correct category ID.
    """
    mock_category = {"id": "123", "title": "Food"}
    mock_repos["category_repo"].get_by_id.return_value = mock_category

    result = category_service.delete_category("123")

    assert result is True
    mock_repos["category_repo"].delete.assert_called_once_with("123")

def test_delete_category_not_found(category_service, mock_repos):
    """
    Test deleting a category that does not exist.
    Ensures False is returned when the category is not found.
    """
    mock_repos["category_repo"].get_by_id.return_value = None

    result = category_service.delete_category("123")

    assert result is False
    mock_repos["category_repo"].delete.assert_not_called()

def test_create_or_update_category_create(category_service, mock_repos):
    """
    Test creating a new category using create_or_update_category.
    Ensures the repository's create method is called when the category does not exist.
    """
    new_category = {"title": "New Category", "description": "New Description"}
    mock_repos["category_repo"].create.return_value = new_category

    result = category_service.create_or_update_category(new_category)

    assert result == new_category
    mock_repos["category_repo"].create.assert_called_once_with(new_category)

def test_create_or_update_category_update(category_service, mock_repos):
    """
    Test updating an existing category using create_or_update_category.
    Ensures the repository's update_category method is called with the correct arguments.
    """
    existing_category = {"id": "123", "title": "Updated Category", "description": "Updated Description"}
    mock_repos["category_repo"].update_category.return_value = existing_category

    result = category_service.create_or_update_category(existing_category)

    assert result == existing_category
    mock_repos["category_repo"].update_category.assert_called_once_with("123", existing_category)