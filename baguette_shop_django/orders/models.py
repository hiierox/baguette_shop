from django.db import models


class Order(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'В обработке'), ('Shipped', 'Отправлен'),
                                                      ('delivered', 'Доставлен')])
    delivery_address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    arrival_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2) # price of one item
    quantity = models.IntegerField()
