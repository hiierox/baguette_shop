from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'price']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'delivery_address', 'total_price', 'paid', 'arrival_date', 'created_at')
    search_fields = ('user',)
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        # Поддержка ручного редактирования
        super().save_model(request, obj, form, change)
        # Пересчёт после изменения
        total = sum(item.price * item.quantity for item in obj.orderitem_set.all())
        obj.total_price = total
        obj.save()