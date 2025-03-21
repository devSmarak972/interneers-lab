from django.db import models
import mongoengine as me
from datetime import datetime
from mongoengine.errors import ValidationError

class ProductCategory(me.Document):
    """
    Represents a category for products, e.g., Food, Kitchen Essentials.
    """
    # id = me.IntField(primary_key=True)  # Explicit integer primary key
    title = me.StringField(required=True, max_length=255, unique=True)
    description = me.StringField()
    meta = {'collection': 'product_categories'}
    
    # @classmethod
    # def generate_next_id(cls):
    #     """Fetch the highest current ID and increments it for uniqueness."""
    #     last_product = cls.objects.order_by('-id').first()
    #     return (last_product.id + 1) if last_product else 1

    # def save(self, *args, **kwargs):
    #     """Ensure a new product gets a unique integer ID if not set."""
    #     if not self.id:
    #         self.id = self.generate_next_id()
    #     super().save(*args, **kwargs)

class Product(me.Document):
    """
    Represents a product with details such as category, price, brand, and quantity.
    """
    # id = me.IntField(primary_key=True)  # Explicit integer primary key
    name = me.StringField(required=True, max_length=255)
    description = me.StringField()
    category = me.ReferenceField(ProductCategory, required=True)
    price = me.FloatField(required=True)
    brand = me.StringField(required=True, max_length=100)
    quantity = me.IntField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'products'}
    def clean(self):
        # Ensure the referenced ProductCategory exists
        if not ProductCategory.objects(id=self.category.id).first():
            raise ValidationError(f"ProductCategory with id {self.category.id} does not exist.")
        
    # @classmethod
    # def generate_next_id(cls):
    #     """Fetch the highest current ID and increments it for uniqueness."""
    #     last_product = cls.objects.order_by('-id').first()
    #     return (last_product.id + 1) if last_product else 1

    # def save(self, *args, **kwargs):
    #     """Ensure a new product gets a unique integer ID if not set."""
    #     if not self.id:
    #         self.id = self.generate_next_id()
    #     super().save(*args, **kwargs)