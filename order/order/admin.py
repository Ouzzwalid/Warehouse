from django.contrib import admin
from .models import Customer, Order, OrderItems

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendeur', 'products', 'customer')

    def products(self, obj):
        return "\n-".join([p.name for p in obj.product.all()])

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)