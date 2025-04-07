import os
import sys
parent_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(0, parent_dir)
print(parent_dir,"seed")
from models import ProductCategory

def seed_categories():
    default_categories = [
        {"title": "Uncategorized", "description": "Default fallback category."},
        {"title": "Food", "description": "Groceries and edible items."},
        {"title": "Kitchen Essentials", "description": "Basic kitchen tools and supplies."},
    ]

    for cat in default_categories:
        if not ProductCategory.objects(title=cat["title"]).first():
            ProductCategory(**cat).save()
