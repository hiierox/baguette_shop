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
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # эту дату где то потом надо будет вычислять на основе адреса и варианта доставки -
    # подключаться к сервисам доставки?
    # создать для этого заглушку пока
    arrival_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # сразу сохраняется Order чтобы получить pk чтобы высчитывать total price из orderitem
        super().save(*args, **kwargs)
        self.total_price = sum(
            item.price * item.quantity for item in self.orderitem_set.all()
                               ) if self.orderitem_set.exists() else 0
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price of one item
    quantity = models.IntegerField()
