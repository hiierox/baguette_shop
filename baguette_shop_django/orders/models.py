from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
                              choices=[('pending', 'В обработке'), ('awaiting dispatch', 'Ждет отправки'),
                                       ('Shipped', 'Отправлен'),
                                       ('delivered', 'Доставлен')])
    delivery_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    arrival_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total_price = sum(item.price * item.quantity for item in self.orderitem_set.all())
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price of one item
    quantity = models.IntegerField()
