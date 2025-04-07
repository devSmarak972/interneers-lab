import unittest
from rest_framework.test import APIClient
from mongoengine import connect, disconnect
import os
import sys
parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(0, parent_dir)
print(parent_dir,"tests")
from tests.seed.seed_data import seed_categories


class TestProductAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        seed_categories()

    def tearDown(self):
        # You can optionally clear DB here
        pass

    def test_create_and_fetch_category(self):
        response = self.client.post("/product/api/cat/", {"title": "Beverages", "description": "Drinks"}, format='json')
        self.assertEqual(response.status_code, 201)

        fetch = self.client.get("/product/api/cat/")
        self.assertEqual(fetch.status_code, 200)
        self.assertTrue(any(cat['title'] == 'Beverages' for cat in fetch.data))

    def test_create_product_with_category(self):
        category_res = self.client.post("/product/api/cat/", {"title": "Stationery", "description": "Office supplies"}, format='json')
        category_id = category_res.data["id"]

        product_data = {
            "name": "Pen",
            "description": "Blue ink ballpoint",
            "price": 5.0,
            "quantity": 100,
            "brand": "Cello",
            "category": category_id
        }
        product_res = self.client.post("/product/api/", product_data, format='json')
        self.assertEqual(product_res.status_code, 201)
        fetch_all = self.client.get("/product/api/")
        self.assertEqual(fetch_all.status_code, 200)
        print(fetch_all.data, "product_res")
        self.assertTrue(any(prod["name"] == "Pen" for prod in fetch_all.data["results"]))

    def test_fetch_products_by_category(self):
        category_res = self.client.post("/product/api/cat/", {"title": "Toys", "description": "Fun stuff"}, format='json')
        category_id = category_res.data["id"]
        prod_res=self.client.post("/product/api/", {
            "name": "Car Toy",
            "description": "Remote control car",
            "price": 99.99,
            "quantity": 10,
            "brand": "HotWheels",
        }, format='json')
        prod_id = prod_res.data["id"]
        prod_cat_res=self.client.post(f"/product/api/cat/{category_id}/p/{prod_id}", {}, format='json')

        self.assertEqual(prod_cat_res.status_code, 200)
        res = self.client.get(f"/product/api/cat/{category_id}")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(any(prod["name"] == "Car Toy" for prod in res.data))

    def test_delete_category_should_update_product_to_uncategorized(self):
        # Create and assign category
        category = self.client.post("/product/api/cat/", {"title": "Snacks", "description": "Chips and cookies"}, format='json').data
        prod = self.client.post("/product/api/", {
            "name": "Cookies", "description": "Chocolate", "price": 20,
            "quantity": 40, "brand": "Oreo", "category": category["id"]
        }, format='json').data

        # Delete category
        self.client.delete(f"/product/api/cat/{category['id']}")

        # Check product updated
        updated = self.client.get(f"/product/api/d/{prod['id']}/")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data['category']['title'], "Uncategorized")

    def test_filter_products(self):
        cat1 = self.client.post("/product/api/cat/", {"title": "Tech", "description": "Electronics"}, format='json').data
        cat2 = self.client.post("/product/api/cat/", {"title": "Books", "description": "Knowledge"}, format='json').data

        p1=self.client.post("/product/api/", {
            "name": "Laptop", "description": "Gaming", "price": 1200,
            "quantity": 5, "brand": "ASUS", "category": cat1["id"]
        }, format='json').data
        pc1=self.client.post(f"/product/api/cat/{cat1["id"]}/p/{p1["id"]}", {}, format='json').data

        p2=self.client.post("/product/api/", {
            "name": "Book", "description": "Fiction", "price": 200,
            "quantity": 30, "brand": "Penguin", "category": cat2["id"]
        }, format='json').data
        pc2=self.client.post(f"/product/api/cat/{cat2["id"]}/p/{p2["id"]}", {}, format='json').data
        res = self.client.get("/product/api/filter/?categories=" + cat1["id"])
        # print(res.data, "res")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(prod["category"]["title"] == "Tech" for prod in res.data))
