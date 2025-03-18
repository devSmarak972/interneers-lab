from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
