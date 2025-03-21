from rest_framework.serializers import Serializer, CharField, ListField,FloatField, IntegerField, Field, ValidationError
from bson import ObjectId

class ObjectIdField(Field):
    """Custom serializer field to handle MongoDB ObjectId"""

    def to_representation(self, value):
        """Convert ObjectId to string when serializing"""
        return str(value)

    def to_internal_value(self, data):
        """Convert string to ObjectId when deserializing"""
        if ObjectId.is_valid(data):
            return ObjectId(data)
        raise ValidationError("Invalid ObjectId format")

class ProductCategorySerializer(Serializer):
    """
    Serializer for the ProductCategory model.
    """
    id = ObjectIdField(required=False)  # Use the custom ObjectIdField

    title = CharField(max_length=255)
    description = CharField(allow_blank=True, required=False)


class ProductSerializer(Serializer):
    """
    Serializer for the Product model. All fields are optional for flexibility.
    """
    id = ObjectIdField(required=False)  # Use the custom ObjectIdField
    name = CharField(max_length=255, required=False)
    description = CharField(allow_blank=True, required=False)
    category = ProductCategorySerializer(read_only=True)
    price = FloatField(required=False)
    brand = CharField(max_length=100, required=False)
    quantity = IntegerField(required=False)

class ProductFilterSerializer(Serializer):
    categories = ListField(
        child=CharField(),
        required=False
    )
    min_price = FloatField(required=False)
    max_price = FloatField(required=False)
    brand = CharField(required=False)
    search = CharField(required=False)

    def validate_categories(self, value):
        """Ensure category IDs are valid ObjectIds."""
        try:
            return [ObjectId(cat) for cat in value]
        except Exception:
            raise ValidationError("Invalid category ID format.")