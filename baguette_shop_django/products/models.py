from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = 'Катеогрия'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    material = models.CharField(max_length=100, verbose_name='Материал')
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Изображение')
    categories = models.ManyToManyField(Category, verbose_name='Категории')
    stock = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество на складе')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name