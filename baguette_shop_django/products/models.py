from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    material = models.CharField(max_length=100)
    width = models.FloatField()
    height = models.FloatField()
    image = models.ImageField(upload_to='products')
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
