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
        super().save_model(request, obj, form, change)
        # total = sum(
        #     item.price * item.quantity for item in obj.orderitem_set.all()
        #             ) if obj.orderitem_set.exists() else 0
        # obj.total_price = total
        # obj.save(update_fields=['total_price'])

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        # Пересчёт total_price после сохранения OrderItem
        total = sum(item.price * item.quantity for item in
                    form.instance.orderitem_set.all()) if form.instance.orderitem_set.exists() else 0
        form.instance.total_price = total
        form.instance.save(update_fields=['total_price'])