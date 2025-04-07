# import unittest
# from unittest.mock import MagicMock
# import sys
# import os
# parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
# sys.path.insert(0, parent_dir)
# print(parent_dir)
# from services  import ProductService

# class TestProductService(unittest.TestCase):
#     def setUp(self):
#         self.mock_repo = MagicMock()
#         self.service = ProductService(repository=self.mock_repo)

#     def test_get_product_by_id(self):
#         mock_product = MagicMock()
#         self.mock_repo.get_product_by_id.return_value = mock_product
#         result = self.service.get_product_by_id("123")
#         self.assertEqual(result, mock_product)
#         self.mock_repo.get_product_by_id.assert_called_once_with("123")


import pytest
from unittest.mock import patch
from django.forms.models import model_to_dict

import sys
import os
parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(0, parent_dir)
from services import ProductService

import pytest
from unittest.mock import MagicMock

def test_create_product():
    # Arrange: Create a mock repository and mock product data
    mock_repo = MagicMock()
    mock_product = {
        "name": "Pen",
        "brand": "Cello",
        "price": 10.0,
        "description": "Blue ink ballpoint",
        "quantity": 100
    }
    mock_repo.create.return_value = mock_product

    # Create a ProductService instance with the mocked repository
    product_service = ProductService(product_repository=mock_repo)

    # Act: Call the create_product method
    data = {
        "name": "Pen",
        "brand": "Cello",
        "price": 10.0,
        "description": "Blue ink ballpoint",
        "quantity": 100
    }
    result = product_service.create_product(data)

    # Assert: Verify the result and that the repository's create method was called
    assert result == mock_product
    mock_repo.create.assert_called_once_with(data)